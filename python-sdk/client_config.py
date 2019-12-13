#!/usr/bin/env python
# - * - coding: utf - 8 -
import os


class client_config:
    """
    类成员变量，便于用.调用和区分命名空间
    """
    # keyword used to represent the RPC Protocol
    PROTOCOL_RPC = "rpc"
    # keyword used to represent the Channel Protocol
    PROTOCOL_CHANNEL = "channel"
    # --------------------------------------
    # configure below
    contract_info_file = "bin/contract.ini"  # 保存已部署合约信息的文件
    account_keyfile_path = "bin/accounts"  # 保存keystore文件的路径，在此路径下,keystore文件以 [name].keystore命名
    account_keyfile = "pyaccount.keystore"
    account_password = "123456"  # 实际使用时建议改为复杂密码
    fiscoChainId = 1  # 链ID，和要通信的节点*必须*一致
    groupid = 1  # 群组ID，和要通信的节点*必须*一致，如和其他群组通信，修改这一项，或者设置bcosclient.py里对应的成员变量
    logdir = "bin/logs"  # 默认日志输出目录，该目录必须先建立
    # ---------client communication config--------------
    client_protocol = "channel"  # or PROTOCOL_CHANNEL to use channel prototol
    # client_protocol = PROTOCOL_CHANNEL
    remote_rpcurl = "http://127.0.0.1:8545"  # 采用rpc通信时，节点的rpc端口,和要通信的节点*必须*一致,如采用channel协议通信，这里可以留空
    channel_host = "127.0.0.1"  # 采用channel通信时，节点的channel ip地址,如采用rpc协议通信，这里可以留空
    channel_port = 20200  # 节点的channel 端口,如采用rpc协议通信，这里可以留空
    channel_ca = "bin/ca.crt"  # 采用channel协议时，需要设置链证书,如采用rpc协议通信，这里可以留空
    channel_node_cert = "bin/sdk.crt"  # 采用channel协议时，需要设置sdk证书,如采用rpc协议通信，这里可以留空
    channel_node_key = "bin/sdk.key"   # 采用channel协议时，需要设置sdk私钥,如采用rpc协议通信，这里可以留空
    # ---------console mode, support user input--------------
    background = True
    # ---------compiler related--------------
    # path of solc compiler
    solc_path = os.environ["HOME"] + "/.py-solc/solc-v0.4.25/bin/solc"
    solcjs_path = "./solcjs"
