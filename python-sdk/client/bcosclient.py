#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/)
  bcosliteclientpy is free software: you can redistribute it and/or modify it under the
  terms of the MIT License as published by the Free Software Foundation. This project is
  distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Thanks for
  authors and contributors of eth-abi, eth-account, eth-hash，eth-keys, eth-typing, eth-utils,
  rlp, eth-rlp , hexbytes ... and relative projects
  @author: kentzhang
  @date: 2019-06
  # reference :https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html
  useful helper:
  int(num,16)  hex -> int
  hex(num)  : int -> hex
'''
from eth_utils.hexadecimal import decode_hex, encode_hex
from eth_account.account import Account
import time
import os
import json
import utils.rpc
from client.common import common
from client.channelpack import ChannelPack
from client.channelhandler import ChannelHandler
from client_config import client_config
from utils.contracts import encode_transaction_data
from client.stattool import StatTool
from client.bcoserror import BcosError, ArgumentsError, BcosException
from client import clientlogger
from utils.contracts import get_function_info
from utils.abi import itertools, get_fn_abi_types_single
from eth_abi import decode_single
from utils.contracts import get_aligned_function_data


class BcosClient:
    client_account = None
    rpc = None
    channel_handler = None
    fiscoChainId = None
    groupid = None
    logger = clientlogger.logger  # logging.getLogger("BcosClient")
    request_counter = itertools.count()
    max_group_id = pow(2, 15) - 1
    max_chain_id = pow(2, 63) - 1
    protocol_list = ["rpc", "channel"]
    sysconfig_keys = ["tx_count_limit", "tx_gas_limit"]

    def __init__(self):
        self.init()
        self.lastblocknum = 0
        self.lastblocklimittime = 0

    def __del__(self):
        """
        release the resources
        """
        self.finish()

    # load the account from keyfile
    def load_default_account(self):
        try:
            with open(self.keystore_file, "r") as dump_f:
                keytext = json.load(dump_f)
                privkey = Account.decrypt(keytext, client_config.account_password)
                self.client_account = Account.from_key(privkey)
        except Exception as e:
            raise BcosException("load account from {} failed, reason: {}"
                                .format(self.keystore_file, e))

    def init(self):
        try:
            self.blockLimit = 500
            # check chainID
            common.check_int_range(client_config.groupid, BcosClient.max_group_id)
            # check group id
            common.check_int_range(client_config.fiscoChainId, BcosClient.max_chain_id)
            # check protocol
            if client_config.client_protocol.lower() not in BcosClient.protocol_list:
                raise BcosException("invalid configuration, must be: {}".
                                    format(''.join(BcosClient.protocol_list)))
            # check account keyfile
            self.keystore_file = "{}/{}".format(client_config.account_keyfile_path,
                                                client_config.account_keyfile)
            if os.path.exists(self.keystore_file) is False:
                raise BcosException(("keystore file {} doesn't exist, "
                                     "please check client_config.py again "
                                     "and make sure this account exist")
                                    .format(self.keystore_file))

            self.fiscoChainId = client_config.fiscoChainId
            self.groupid = client_config.groupid

            if client_config.client_protocol == client_config.PROTOCOL_RPC \
                    and client_config.remote_rpcurl is not None:
                self.rpc = utils.rpc.HTTPProvider(client_config.remote_rpcurl)
                self.rpc.logger = self.logger

            if client_config.client_protocol == client_config.PROTOCOL_CHANNEL:
                if os.path.exists(client_config.channel_node_cert) is False:
                    raise BcosException("{} not found!".format(client_config.channel_node_cert))
                if os.path.exists(client_config.channel_node_key) is False:
                    raise BcosException("{} not found!".format(client_config.channel_node_key))

                self.channel_handler = ChannelHandler()
                self.channel_handler.logger = self.logger
                self.channel_handler.initTLSContext(client_config.channel_ca,
                                                    client_config.channel_node_cert,
                                                    client_config.channel_node_key
                                                    )
                self.channel_handler.start_channel(
                    client_config.channel_host, client_config.channel_port)
                blockNumber = self.getBlockNumber()
                self.channel_handler.setBlockNumber(blockNumber)
                self.channel_handler.getBlockNumber(self.groupid)

            self.logger.info("using protocol " + client_config.client_protocol)
            return self.getinfo()
        except Exception as e:
            raise BcosException("init bcosclient failed, reason: {}".format(e))

    def finish(self):
        if client_config.client_protocol == client_config.PROTOCOL_CHANNEL \
           and self.channel_handler is not None:
            self.channel_handler.finish()

    def getinfo(self):
        info = ""
        if client_config.client_protocol == client_config.PROTOCOL_RPC:
            info = "rpc:{}\n".format(self.rpc)
        if client_config.client_protocol == client_config.PROTOCOL_CHANNEL:
            info = "channel {}:{}".format(self.channel_handler.host, self.channel_handler.port)
        info += ",groupid :{}\n".format(self.groupid)
        if self.client_account is not None:
            info += "account address: {}\n".format(self.client_account.address)
        return info

    def is_error_response(self, response):
        if response is None:
            raise BcosError(-1, None, "response is None")
        result = response["result"]
        if isinstance(result, dict) and "error" in result.keys():
            msg = result["error"]["message"]
            code = result["error"]["code"]
            data = None
            if("data" in result["error"]):
                data = result["error"]["data"]
            self.logger.error("is_error_response code: {}, msg:{} ,data:{}".format(code, msg, data))
            raise BcosError(code, data, msg)
        return None

    def common_request(self, cmd, params, packet_type=ChannelPack.TYPE_RPC):
        response = None
        try:
            next(self.request_counter)
            stat = StatTool.begin()
            if client_config.client_protocol == client_config.PROTOCOL_RPC:
                response = self.rpc.make_request(cmd, params)
            if client_config.client_protocol == client_config.PROTOCOL_CHANNEL:
                response = self.channel_handler.make_request(
                    cmd, params, ChannelPack.TYPE_RPC, packet_type)
            self.is_error_response(response)
            memo = "DONE"
            stat.done()
            stat.debug("commonrequest:{}:{}".format(cmd, memo))
            return response["result"]
        except Exception as e:
            # timeout exception
            exception_str = str(e).lower()
            if "timeout" in exception_str:
                raise BcosException(("{} timeout for without response after 60s, "
                                     "please check the status of the node").format(cmd))
            else:
                raise BcosError(-1, None, ("{} failed,"
                                           " params: {}, response: {}, error information: {}").
                                format(cmd, params, json.dumps(response), e))

    def getNodeVersion(self):
        """
        get node version
        // Request
        curl -X POST --data '{"jsonrpc":"2.0","method":"getClientVersion",
        "params":[],"id":1}' http://127.0.0.1:8545 |jq
        // Response
        {
        "id": 83,
        "jsonrpc": "2.0",
        "result": {
            "Build Time": "20190106 20:49:10",
            "Build Type": "Linux/g++/RelWithDebInfo",
            "FISCO-BCOS Version": "2.0.0",
            "Git Branch": "master",
            "Git Commit Hash": "693a709ddab39965d9c39da0104836cfb4a72054"
        }
        }
        """
        cmd = "getClientVersion"
        params = []
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getblocknumber
    def getBlockNumber(self):
        cmd = "getBlockNumber"
        params = [self.groupid]
        num_hex = self.common_request(cmd, params)
        return int(num_hex, 16)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpbftview
    def getPbftView(self):
        cmd = "getPbftView"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getsealerlist

    def getSealerList(self):
        cmd = "getSealerList"
        params = [self.groupid]
        return self.common_request(cmd, params)
    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getobserverlist

    def getObserverList(self):
        cmd = "getObserverList"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getconsensusstatus
    def getConsensusStatus(self):
        cmd = "getConsensusStatus"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getsyncstatus
    def getSyncStatus(self):
        cmd = "getSyncStatus"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpeers
    def getPeers(self):
        cmd = "getPeers"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getgrouppeers
    def getGroupPeers(self):
        cmd = "getGroupPeers"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getnodeidlist
    def getNodeIDList(self):
        cmd = "getNodeIDList"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getgrouplist
    def getGroupList(self):
        cmd = "getGroupList"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getblockbyhash
    def getBlockByHash(self, block_hash, _includeTransactions=True):
        cmd = "getBlockByHash"
        common.check_hash(block_hash)
        includeTransactions = common.check_and_trans_to_bool(_includeTransactions)
        params = [self.groupid, block_hash, includeTransactions]
        return self.common_request(cmd, params)
    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getblockbynumber

    def getBlockByNumber(self, num, _includeTransactions=True):
        """
        get block according to number
        """
        cmd = "getBlockByNumber"
        number = common.check_int_range(num)
        includeTransactions = common.check_and_trans_to_bool(_includeTransactions)
        params = [self.groupid, hex(number), includeTransactions]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getblockhashbynumber
    def getBlockHashByNumber(self, num):
        cmd = "getBlockHashByNumber"
        common.check_int_range(num)
        params = [self.groupid, hex(num)]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_cn/release-2.0/docs/api.html#gettransactionbyhash
    def getTransactionByHash(self, hash):
        cmd = "getTransactionByHash"
        common.check_hash(hash)
        params = [self.groupid, hash]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#gettransactionbyblockhashandindex
    def getTransactionByBlockHashAndIndex(self, hash, index):
        cmd = "getTransactionByBlockHashAndIndex"
        common.check_hash(hash)
        common.check_int_range(index)
        params = [self.groupid, hash, hex(index)]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#gettransactionbyblocknumberandindex
    def getTransactionByBlockNumberAndIndex(self, num, index):
        cmd = "getTransactionByBlockNumberAndIndex"
        common.check_int_range(num)
        common.check_int_range(index)
        params = [self.groupid, hex(num), hex(index)]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#gettransactionreceipt
    def getTransactionReceipt(self, hash):
        cmd = "getTransactionReceipt"
        common.check_hash(hash)
        params = [self.groupid, hash]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpendingtransactions
    def getPendingTransactions(self):
        cmd = "getPendingTransactions"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpendingtxsize
    def getPendingTxSize(self):
        cmd = "getPendingTxSize"
        params = [self.groupid]
        tx_size = self.common_request(cmd, params)
        return int(tx_size, 16)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getcode
    def getCode(self, address):
        cmd = "getCode"
        fmt_addr = common.check_and_format_address(address)
        params = [self.groupid, fmt_addr]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#gettotaltransactioncount
    def getTotalTransactionCount(self):
        cmd = "getTotalTransactionCount"
        params = [self.groupid]
        return self.common_request(cmd, params)

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getsystemconfigbykey
    def getSystemConfigByKey(self, key):
        if key not in BcosClient.sysconfig_keys:
            raise ArgumentsError("invalid system key, must be {}"
                                 .format(BcosClient.sysconfig_keys))
        cmd = "getSystemConfigByKey"
        params = [self.groupid, key]
        return self.common_request(cmd, params)

    def channel_getBlockLimit(self):
        """
        get blockNumber from _block_notify directly when use channelHandler
        """
        return self.channel_handler.blockNumber + self.blockLimit

    def RPC_getBlocklimit(self):
        tick = time.time()
        deltablocklimit = 500
        tickstamp = tick - self.lastblocklimittime
        self.logger.debug("blocklimit tick stamp {}".format(tickstamp))
        if tickstamp < 100:  # get blocklimit every 100sec
            return self.lastblocknum + deltablocklimit
        for i in range(0, 5):  # try n times
            try:

                blocknum = self.getBlockNumber()
                oldblocknum = self.lastblocknum
                # print("last {},now {}".format(self.lastblocknum,blocknum))
                if blocknum >= self.lastblocknum:
                    self.lastblocknum = blocknum
                    self.logger.info("getBlocklimit:{},blocknum:{},old:{}".format(
                        self.lastblocknum, blocknum, oldblocknum))
                    return self.lastblocknum + deltablocklimit
            except BcosError as e:
                self.logger.error("getBlocklimit error {}, {}".format(e.code, e.message))
                time.sleep(0.2)

                continue
        return self.lastblocknum

    def getBlockLimit(self):
        """
        get block limit
        """
        if self.channel_handler is not None:
            return self.channel_getBlockLimit()
        return self.RPC_getBlocklimit()

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpendingtransactions

    def call(self, to_address, contract_abi, fn_name, args=None):
        cmd = "call"
        if to_address != "":
            common.check_and_format_address(to_address)
        if self.client_account is None:
            self.load_default_account()
        functiondata = encode_transaction_data(fn_name, contract_abi, None, args)
        callmap = dict()
        callmap["data"] = functiondata
        callmap["from"] = self.client_account.address
        callmap["to"] = to_address
        callmap["value"] = 0
        # send transaction to the given group
        params = [client_config.groupid, callmap]
        # 发送
        response = self.common_request(cmd, params)
        if "output" in response.keys():
            outputdata = response["output"]
            # 取得方法的abi，签名，参数 和返回类型，进行call返回值的解析
            fn_abi, fn_selector, fn_arguments = get_function_info(
                fn_name, contract_abi, None, args, None,
            )
            # print("fn_selector",fn_selector)
            # print("fn_arguments",fn_arguments)
            fn_output_types = get_fn_abi_types_single(fn_abi, "outputs")
            # print("output types str:", fn_output_types)
            decoderesult = decode_single(fn_output_types, decode_hex(outputdata))
            return decoderesult
        return response

    # https://fisco-bcos-documentation.readthedocs.io/zh_CN/release-2.0/docs/api.html#getpendingtransactions
    '''
        可用于所有已知abi的合约，传入abi定义，方法名，正确的参数列表，即可发送交易。交易由BcosClient里加载的账号进行签名。
    '''

    def sendRawTransaction(self, to_address, contract_abi, fn_name, args=None,
                           bin_data=None, gasPrice=30000000,
                           packet_type=ChannelPack.TYPE_RPC):
        cmd = "sendRawTransaction"
        if to_address != "":
            common.check_and_format_address(to_address)
        # 第三个参数是方法的abi，可以传入None，encode_transaction_data做了修改，支持通过方法+参数在整个abi里找到对应的方法abi来编码

        if bin_data is None:
            functiondata = encode_transaction_data(fn_name, contract_abi, None, args)
        # the args is None
        elif args is None:
            functiondata = bin_data
        # deploy with params
        else:
            fn_data = get_aligned_function_data(contract_abi, None, args)
            functiondata = bin_data + fn_data[2:]

        if to_address is not None and len(to_address) > 0:
            from eth_utils import to_checksum_address
            to_address = to_checksum_address(to_address)

        # load default account if not set .notice: account only use for
        # sign transaction for sendRawTransaction
        if self.client_account is None:
            self.load_default_account()
        # 填写一个bcos transaction 的 mapping
        import random
        txmap = dict()
        txmap["randomid"] = random.randint(0, 1000000000)  # 测试用 todo:改为随机数
        txmap["gasPrice"] = gasPrice
        txmap["gasLimit"] = gasPrice
        txmap["blockLimit"] = self.getBlockLimit()  # 501  # 测试用，todo：从链上查一下

        txmap["to"] = to_address
        txmap["value"] = 0
        txmap["data"] = functiondata
        txmap["fiscoChainId"] = self.fiscoChainId
        txmap["groupId"] = self.groupid
        txmap["extraData"] = ""
        '''
        from datatypes.bcostransactions import (
            serializable_unsigned_transaction_from_dict,
        )
        # 将mapping构建一个transaction对象,非必要，用来对照的
        transaction = serializable_unsigned_transaction_from_dict(txmap)
        # 感受下transaction encode的原始数据
        print(encode_hex(rlp.encode(transaction)))
        '''

        # 实际上只需要用sign_transaction就可以获得rawTransaction的编码数据了,input :txmap,私钥
        signedTxResult = Account.sign_transaction(txmap, self.client_account.privateKey)
        # signedTxResult.rawTransaction是二进制的，要放到rpc接口里要encode下
        params = [self.groupid, encode_hex(signedTxResult.rawTransaction)]
        result = self.common_request(cmd, params, packet_type)
        return result

    # 发送交易后等待共识完成，检索receipt
    def channel_sendRawTransactionGetReceipt(self, to_address, contract_abi,
                                             fn_name, args=None, bin_data=None, gasPrice=30000000,
                                             timeout=15):
        return self.sendRawTransaction(to_address, contract_abi, fn_name, args, bin_data, gasPrice,
                                       ChannelPack.TYPE_TX_COMMITTED)

    def rpc_sendRawTransactionGetReceipt(self, to_address, contract_abi,
                                         fn_name, args=None, bin_data=None, gasPrice=30000000,
                                         timeout=15):
        # print("sendRawTransactionGetReceipt",args)
        stat = StatTool.begin()
        txid = self.sendRawTransaction(to_address, contract_abi, fn_name, args, bin_data, gasPrice)
        result = None
        for i in range(0, timeout):
            result = self.getTransactionReceipt(txid)
            # print("getTransactionReceipt : ", result)
            if result is None:
                time.sleep(1)
                self.logger.info(
                    "sendRawTransactionGetReceipt,retrying getTransactionReceipt : {}".format(i))
                continue
            else:
                break  # get the result break
        stat.done()
        memo = "DONE"
        if result is None:
            memo = "ERROR:TIMEOUT"
        stat.debug("sendRawTransactionGetReceipt,{}".format(memo))
        if result is None:
            raise BcosError(-1, None, "sendRawTransactionGetReceipt,{}".format(memo))
        return result

    def sendRawTransactionGetReceipt(self, to_address, contract_abi,
                                     fn_name, args=None, bin_data=None, gasPrice=30000000,
                                     timeout=15):
        if self.channel_handler is not None:
            return self.channel_sendRawTransactionGetReceipt(to_address, contract_abi,
                                                             fn_name, args, bin_data,
                                                             gasPrice, timeout)

        return self.rpc_sendRawTransactionGetReceipt(to_address, contract_abi,
                                                     fn_name, args, bin_data,
                                                     gasPrice, timeout)

    '''
        newaddr = result['contractAddress']
        blocknum = result['blockNumber']
    '''

    def deploy(self, contract_bin):
        result = self.sendRawTransactionGetReceipt(
            to_address="", contract_abi=None, fn_name=None, bin_data=contract_bin)
        # newaddr = result['contractAddress']
        # blocknum = result['blockNumber']
        # print("onblock : %d newaddr : %s "%(int(blocknum,16),newaddr))
        return result

    def deployFromFile(self, contractbinfile):
        with open(contractbinfile, "r") as f:
            contractbin = f.read()
        result = self.deploy(contractbin)
        return result
