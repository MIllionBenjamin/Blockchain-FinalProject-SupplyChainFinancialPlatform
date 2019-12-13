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
'''

# codec for abi,block,transaction,receipt,logs
import json
from eth_abi import decode_single
from eth_utils import (
    function_signature_to_4byte_selector,
    event_abi_to_log_topic,
    encode_hex, decode_hex)

from utils.abi import (
    filter_by_type,
    abi_to_signature,
    get_fn_abi_types_single,
    exclude_indexed_event_inputs_to_single)


class DatatypeParser:
    contract_abi = None
    func_abi_map_by_selector = dict()
    func_abi_map_by_name = dict()
    event_abi_map = dict()

    def __init__(self, abi_file=None):
        if abi_file is not None:
            self.load_abi_file(abi_file)

    def from_text(self, abitext):
        self.contract_abi = json.loads(abitext)
        self.parse_abi()

    def set_abi(self, abi):
        self.contract_abi = abi
        self.parse_abi()

    def load_abi_file(self, abi_file):
        with open(abi_file, 'r') as load_f:
            contract_abi = json.load(load_f)
            load_f.close()
            self.set_abi(contract_abi)


    def parse_abi(self):
        '''for item in self.contract_abi:
            if (item["type"] != "constructor"):
                print(item["name"], " is a ", item["type"])
                hash4 = function_signature_to_4byte_selector(item["name"] + '()')
                print("function hash4:", encode_hex(hash4))'''
        funclist = filter_by_type("function", self.contract_abi)
        for func in funclist:
            signature = abi_to_signature(func)
            selector = function_signature_to_4byte_selector(signature)
            # print(func)
            # print(signature)
            # print(encode_hex(selector) )
            self.func_abi_map_by_selector[encode_hex(selector)] = func
            self.func_abi_map_by_name[func['name']] = func

        eventlist = filter_by_type("event", self.contract_abi)
        for event in eventlist:
            topic = event_abi_to_log_topic(event)
            # print(event)
            # print(encode_hex(topic) )
            self.event_abi_map[encode_hex(topic)] = event

    # 用于receipt，解析eventlog数组，在原数据中增加解析后的 eventname，eventdata两个数据
    def parse_event_logs(self, logs):
        # print(self.event_abi_map)
        for log in logs:
            if(len(log["topics"]) == 0):  # 匿名event
                continue
            topic = log["topics"][0]
            if topic not in self.event_abi_map:
                continue
            eventabi = self.event_abi_map[topic]
            # print(eventabi)
            if eventabi is None:
                continue
            # args_abi = get_fn_abi_types(eventabi,'inputs')
            argslist = exclude_indexed_event_inputs_to_single(eventabi)
            # print(argslist)
            result = decode_single(argslist, decode_hex(log['data']))
            # print(result)
            log["eventdata"] = result
            log["eventname"] = eventabi["name"]
        return logs

    # 用于transaction，用于查询交易后解析input数据（方法+参数）
    # 返回 result['name'] result['args']
    def parse_transaction_input(self, inputdata):
        selector = inputdata[0:10]
        argsdata = inputdata[10:]
        # print(selector)
        # print(self.func_abi_map_by_selector.keys())
        if selector not in self.func_abi_map_by_selector:
            return None
        func_abi = self.func_abi_map_by_selector[selector]
        # print(func_abi)
        args_abi = get_fn_abi_types_single(func_abi, "inputs")
        args = decode_single(args_abi, decode_hex(argsdata))
        result = dict()
        result['name'] = func_abi["name"]
        result['args'] = args
        result['signature'] = abi_to_signature(func_abi)
        return result

    # 用于receipt，解析合约接口的返回值
    # 取决于接口定义
    def parse_receipt_output(self, name, outputdata):
        if name not in self.func_abi_map_by_name:
            return None
        func_abi = self.func_abi_map_by_name[name]
        output_args = get_fn_abi_types_single(func_abi, "outputs")
        # print(output_args)
        result = decode_single(output_args, decode_hex(outputdata))
        return result

    def get_func_signature(self, name):
        if(name not in self.func_abi_map_by_name):
            return None
        # abi = self.func_abi_map_by_name[name]
        return abi_to_signature(name)
