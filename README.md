# 基于区块链的供应链金融平台
> 使用[FISCO BCOS](https://github.com/FISCO-BCOS/FISCO-BCOS)
<br>


- [基于区块链的供应链金融平台](#%e5%9f%ba%e4%ba%8e%e5%8c%ba%e5%9d%97%e9%93%be%e7%9a%84%e4%be%9b%e5%ba%94%e9%93%be%e9%87%91%e8%9e%8d%e5%b9%b3%e5%8f%b0)
  - [一、依赖环境](#%e4%b8%80%e4%be%9d%e8%b5%96%e7%8e%af%e5%a2%83)
    - [1. 链端与后端](#1-%e9%93%be%e7%ab%af%e4%b8%8e%e5%90%8e%e7%ab%af)
    - [2. 前端](#2-%e5%89%8d%e7%ab%af)
  - [二、文件说明](#%e4%ba%8c%e6%96%87%e4%bb%b6%e8%af%b4%e6%98%8e)
  - [三、运行](#%e4%b8%89%e8%bf%90%e8%a1%8c)
  - [四、补充](#%e5%9b%9b%e8%a1%a5%e5%85%85)
  - [English Introduction](#english-introduction)


## 一、依赖环境

### 1. 链端与后端
- Ubuntu 18.04
- [FISCO BCOS v2.1.0](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/installation.html)
- Python 3.6.3+
- [FISCO BCOS Python SDK](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/python_sdk/install.html)
- [Flask 1.1](http://flask.palletsprojects.com/en/1.1.x/)

### 2. 前端
- MacOS
- Xcode

## 二、文件说明
- 链端：[Loan.sol](./Loan.sol) 合约中实现完整供应链金融平台逻辑
- 后端：[python-sdk/Loan_contract_invoke.py](./python-sdk/Loan_contract_invoke.py)实现对Loan合约调用的封装；[python-sdk/Loan_contract_flask_backend.py](./python-sdk/Loan_contract_flask_backend.py)运行服务端，接受外部请求并返回JSON数据
- 前端：[Loan_UI](./Loan_UI)中是一个完整的iOSApp工程


## 三、运行
Ubuntu配置好依赖环境后，将 `Loan.sol` 部署到节点上，若成功部署，会得到 __合约地址__。你可以先在控制台中调用合约，产生一些实例以及发送交易。

用得到的合约地址替换 `python-sdk/Loan_contract_flask_backend.py`，`Line 9` 中的地址，将语句改为：
``` python
loan_contract = Loan_Contract(address=your_new_address)
```
注意保留双引号

假设在你的Ubuntu中，FISCO BCOS Python SDK路径为 `$FB-Python-SDK`。
<br>
将 `Loan.sol` 复制到你的 `$FB-Python-SDK/contracts` 中；
<br>
将 `python-sdk/Loan_contract_invoke.py` 和 `python-sdk/Loan_contract_flask_backend.py` 复制到你的 `$FB-Python-SDK` 中


此时运行 Loan_contract_flask_backend.py，服务端会在8383端口监听请求。
<br>
请求示例：
<br>
- 获取名称为A的公司的信息
```
GET: {IP}:8383/get_company_inf/?cpName=A
```
- 获取所有公司A参与交易的单据
```
GET: {IP}:8383/get_receipt/?cpName=A
```
- 获取银行bank_1向公司A提供的信用资产的数额
```
GET: {IP}:8383/get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany/?bName=bank_1&cpName=A
```

在MacOS中打开 `Loan_UI/Loan_UI.xcworkspace`，在Xcode点击运行按钮即可使用前端界面。
<br>
注意修改 `Loan_UI/Loan_UI/SearchCompanyPage/SearchCompanyViewController.m`，`Loan_UI/Loan_UI/SearchReceiptPage/SearchReceiptViewController.m` 和 `Loan_UI/Loan_UI/SearchCreditAssetPage` 里的URL


## 四、补充
背景介绍、方案设计和功能测试等详见 `17343107_王明业.pdf`。
<br>
Demo见本目录下的.mp4视频。

## English Introduction

An independent work. Finish the whole platform including the front end, the back end and the chain end. Use the consortium blockchain platform [FISCO-BCOS](https://github.com/FISCO-BCOS/FISCO-BCOS) maintained by Tencent.

Consider the following scenario:

There are three companies A, B and C. 
Company A has a large scale, good credit, great risk-bearing capacity, and is qualified to directly obtain large amounts of financing from banks and other financial institutions.

Companies B and C are small and cannot obtain large amount of money directly from any financial institutions.

Now Company A orders a batch of goods from company B. Company B needs to order supplementary materials from company C to produce this batch of goods.

Company A is currently short of funds. A document signed by company A is sent to company B, promising to pay company B for the goods. At this time, company B can use this document to get a loan from the bank, With the credit of company A. 

And company B can sign a document to company C in the same way. Company C can get a loan from the bank through the document.

Under the traditional method, such a process requires a very complicated authorization and verification process.

This project uses blockchain technology to efficiently implement such a credit transfer process and realize a blockchain-based supply chain financial platform.

