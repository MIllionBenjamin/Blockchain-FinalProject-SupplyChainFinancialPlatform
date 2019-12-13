### v0.9.0

(2019-08-16)

**新特性** 

- 提供调用FISCO BCOS 2.0 JSON-RPC的Python API。
- 可基于Channel协议与FISCO BCOS进行通信，保证节点与SDK安全加密通信的同时，接收节点推送的消息。
- 支持交易解析功能：包括交易输入、交易输出、Event Log等ABI数据的拼装和解析。
- 支持合约编译，将sol合约编译成abi和bin文件。
- 支持基于keystore的账户管理。