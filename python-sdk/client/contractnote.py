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
from client_config import client_config
from configobj import ConfigObj
import time
import os


class ContractNote:
    @staticmethod
    def get_last(name):
        config = ConfigObj(client_config.contract_info_file, encoding='UTF8')
        if name in config["address"]:
            address = config["address"][name]
        else:
            address = None
        return address

    @staticmethod
    def save_address(contractname, newaddress, blocknum=None, memo=None):

        # write to file
        config = ConfigObj(client_config.contract_info_file,
                           encoding='UTF8')
        if 'address' not in config:
            # print("address not in config",config)
            config['address'] = {}

        config['address'][contractname] = newaddress
        # print (config)
        if blocknum is not None:
            if "history" not in config:
                config["history"] = {}
            timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            detail = "{}:{},block:{}".format(contractname, timestr, blocknum)
            if memo is not None:
                detail = "{},{}".format(detail, memo)
            config["history"][newaddress] = detail
        config.write()

    @staticmethod
    def save_contract_address(contract_name, newadddress):
        """
        record the deployed contract address to the file
        """
        cache_dir = ".cache/"
        if os.path.exists(cache_dir) is False:
            os.makedirs(cache_dir)
        cache_file = cache_dir + contract_name
        fp = open(cache_file, 'a')
        fp.write(newadddress + "\n")
        fp.close()

    @staticmethod
    def get_contract_addresses(contract_name):
        """
        get contract address according to the file
        """
        cache_dir = ".cache/"
        cache_file = cache_dir + contract_name
        if os.path.exists(cache_file) is False:
            return None
        # get addresses
        fp = open(cache_file, 'r')
        lines = fp.readlines()
        contract_addresses = []
        for line in lines:
            line = line.strip('\n')
            contract_addresses.append(line)
        fp.close()
        return contract_addresses
