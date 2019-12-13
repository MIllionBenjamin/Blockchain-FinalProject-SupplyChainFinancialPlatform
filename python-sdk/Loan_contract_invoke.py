#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  @author: MillionBenjamin(Mingye Wang)
  @email: millionbenjaminwang@gmail.com
'''
from client.contractnote import ContractNote
from client.bcosclient import BcosClient
import os
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client.bcoserror import BcosException, BcosError
from client_config import client_config


class Loan_Contract:
    
    def __init__(self, address: str):
        # 从文件加载abi定义
        # Now file has been complied. Use .abi directly.
        
        if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
            Compiler.compile_file("contracts/Loan.sol")
        
        abi_file = "contracts/Loan.abi"
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        self.contract_abi = data_parser.contract_abi

        self.client = BcosClient()

        self.to_address = address


    def get_bank_info_by_index(self, index: int):
        bank_inf = self.client.call(self.to_address, self.contract_abi, "banks", [index])
        return {"bankName": bank_inf[0]}
    
    
    def get_company_info_by_index(self, index: int):
        cp_inf = self.client.call(self.to_address, self.contract_abi, "companies", [index])
        return {"companyName": cp_inf[0], 
                "companyType": cp_inf[1], 
                "isTrusted": cp_inf[2], 
                "creditAsset": cp_inf[3], 
                "realMoney": cp_inf[4]}


    def get_receipt_info_by_index(self, index: int):
        receipt_inf = self.client.call(self.to_address, self.contract_abi, "receipts", [index])
        return {"Name_A": receipt_inf[0], 
                "Name_B": receipt_inf[1], 
                "bankParticipation": receipt_inf[2], 
                "isRealMoney": receipt_inf[3], 
                "amount": receipt_inf[4]}
    

    def get_bank_inf_by_name(self, bName: str):
        bank_inf = self.client.call(self.to_address, self.contract_abi, "getBankInfoByName", [bName])
        return {"bankName": bank_inf[0]}
        

    def get_company_inf_by_name(self, cpName: str):
        cp_inf = self.client.call(self.to_address, self.contract_abi, "getCompanyInfoByName", [cpName])
        return {"companyName": cp_inf[0], 
                "companyType": cp_inf[1], 
                "isTrusted": cp_inf[2], 
                "creditAsset": cp_inf[3], 
                "realMoney": cp_inf[4]}


    def get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany(self, bName: str, cpName: str):
        result = self.client.call(self.to_address, self.contract_abi, "getAmountOfCreditAsset_bankGiveToTrustedCompany", [bName, cpName])
        return {"amount": result[0]}


    def get_company_num(self):
        result = self.client.call(self.to_address, self.contract_abi, "getCompanyNum")
        return {"companyNum": result[0]}
    
    
    def get_bank_num(self):
        result = self.client.call(self.to_address, self.contract_abi, "getBankNum")
        return {"bankNum": result[0]}
        
        
    def get_receipt_num(self):
        result = self.client.call(self.to_address, self.contract_abi, "getReceiptNum")
        return {"receiptNum": result[0]}


    def exit(self):
        self.client.finish()