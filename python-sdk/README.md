# Python SDK

![](./images/FISCO_BCOS_Logo.svg)


[![Build Status](https://travis-ci.org/FISCO-BCOS/python-sdk.svg?branch=master)](https://travis-ci.org/FISCO-BCOS/python-sdk)
[![CodeFactor](https://www.codefactor.io/repository/github/fisco-bcos/python-sdk/badge)](https://www.codefactor.io/repository/github/fisco-bcos/python-sdk)
[![GitHub license](https://img.shields.io/github/license/FISCO-BCOS/python-sdk.svg)](https://github.com/FISCO-BCOS/python-sdk/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/FISCO-BCOS/python-sdk.svg)](https://github.com/FISCO-BCOS/python-sdk/issues)
--- 

Python SDK为[FISCO BCOS](https://github.com/FISCO-BCOS/FISCO-BCOS/tree/master)提供Python API，使用FISCO BCOS Python SDK可以简单快捷的基于FISCO-BCOS进行区块链应用开发。**此版本只支持**[FISCO BCOS 2.0](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/)。


## 关键特性

- 提供调用FISCO BCOS 2.0 [JSON-RPC](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/api.html)的Python API。
- 可基于[Channel协议](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/design/protocol_description.html#channelmessage)与FISCO BCOS进行通信，保证节点与SDK安全加密通信的同时，可接收节点推送的消息。
- 支持交易解析功能：包括交易输入、交易输出、Event Log等ABI数据的拼装和解析。
- 支持合约编译，将`sol`合约编译成`abi`和`bin`文件。
- 支持基于keystore的账户管理。
- 支持合约历史查询。

## 部署Python SDK

### 环境要求
- Python环境：python 3.6.3, 3.7.x
- FISCO BCOS节点：请参考[FISCO BCOS安装](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/installation.html#fisco-bcos)搭建

### 依赖软件

- **Ubuntu**: `sudo apt install -y zlib1g-dev libffi6 libffi-dev wget git`
- **CentOS**：`sudo yum install -y zlib-devel libffi-devel wget git`
- **MacOs**: `brew install wget npm git`

### 初始化环境(若python环境符合要求，可跳过)

#### **Linux环境初始化**

> 拉取源代码
```bash
git clone https://github.com/FISCO-BCOS/python-sdk
```

> 配置环境(安装pyenv和python，若python版本>=3.6.3可跳过本步)
```bash
# 获取python版本
python --version

## --------若python版本小于3.6.3，执行下面流程--------------------------------------
# 判断python版本，并为不符合条件的python环境安装python 3.7.3的虚拟环境，命名为python-sdk
# 若python环境符合要求，可以跳过此步
# 若脚本执行出错，请检查是否参考[依赖软件]说明安装了依赖
# 提示：安装python-3.7.3可能耗时比较久
cd python-sdk && bash init_env.sh -p

## --------若通过bash init_env.sh -p安装了python-sdk虚拟环境，执行下面流程-------------
# 激活python-sdk虚拟环境
source ~/.bashrc && pyenv activate python-sdk && pip install --upgrade pip
```

#### **Windows环境初始化**

在Windows运行Python SDK，需要按照以下步骤安装依赖软件并配置合约编译器：

**安装依赖软件**

- 直接安装[Python-3.7.x](https://www.python.org/downloads/release/python-373/)和[git](https://git-scm.com/download/win)软件  
> python环境变量配置可参考[这里](https://jingyan.baidu.com/article/b0b63dbff271e24a4830708d.html)

- [Visual C++ 14.0库](https://visualstudio.microsoft.com/downloads)
> (注：Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools"解决方法: https://visualstudio.microsoft.com/downloads （注意选择vs 2005即14.0版）或 https://pan.baidu.com/s/1ZmDUGZjZNgFJ8D14zBu9og 提取码: zrby)

- 下载Windows版本solc, 点击[这里](https://github.com/ethereum/solidity/releases/download/v0.4.25/solidity-windows.zip)下载
> solc编译器下载成功后，解压，将其中的 solc.exe 文件复制 ${python-sdk}\bin 目录下。若 python-sdk 路为 D:\\open-source\\python-sdk, 则 solc.exe 文件复制路径为D:\\open-source\\python-sdk\\bin\\solc.exe 

**拉取源代码**

打开 git，在任意目录执行如下命令
```bash
git clone https://github.com/FISCO-BCOS/python-sdk
```

**配置solc编译器路径**
```bash
# 修改client_config.py.template: 
# 配置solc编译器路径，若solc存放路径为D:\\open-source\\python-sdk\\bin\\solc.exe，则solc_path配置如下：
solc_path = "D:\\open-source\\python-sdk\\bin\\solc.exe"

# 将client_config.py.template拷贝到client_config.py
```

### **安装Python SDK依赖**

```bash
cd python-sdk 
pip install -r requirements.txt
```

> **若因网络原因，安装依赖失败，可使用清华的pip源下载，安装命令如下：**

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 初始化配置(Windows环境可跳过)

```bash
# 该脚本执行操作如下：
# 1. 拷贝client_config.py.template->client_config.py
# 2. 安装solc编译器
bash init_env.sh -i
```

> **若MacOS环境solc安装较慢，可在python-sdk目录下执行如下命令安装solcjs**，python-sdk自动加载nodejs编译器：

```bash
# 安装编译器
npm install solc@v0.4.25
```

> 若没有执行以上初始化步骤，需要将`contracts/`目录下的`sol`代码手动编译成`bin`和`abi`文件并放置于`contracts`目录，才可以部署和调用相应合约。合约编译可以使用[remix](https://remix.ethereum.org)


## 配置Channel通信协议

Python SDK支持使用[Channel协议](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/design/protocol_description.html#channelmessage-v1)与FISCO BCOS节点通信，通过SSL加密通信保障SDK与节点通信的机密性。

设SDK连接的节点部署在目录`~/fisco/nodes/127.0.0.1`目录下，则通过如下步骤使用Channel协议：

**配置Channel信息**

在节点目录下的 config.ini 文件中获取 channel_listen_port, 这里为20200  
```bash
[rpc]
    listen_ip=0.0.0.0
    channel_listen_port=20200
    jsonrpc_listen_port=8545
```
    
切换到python-sdk目录，修改 client_config.py 文件中`channel_host`为实际的IP，`channel_port`为上步获取的`channel_listen_port`：

```bash
channel_host = "127.0.0.1"
channel_port = 20200
```

**配置证书**

```bash
# 若节点与python-sdk位于不同机器，请将节点sdk目录下所有相关文件拷贝到bin目录
# 若节点与sdk位于相同机器，直接拷贝节点证书到SDK配置目录
cp ~/fisco/nodes/127.0.0.1/sdk/* bin/
```

**配置证书路径**

  - `client_config.py`的`channel_node_cert`和`channel_node_key`选项分别用于配置SDK证书和私钥
  - `release-2.1.0`版本开始，SDK证书和私钥更新为`sdk.crt`和`sdk.key`，配置证书路径前，请先检查上步拷贝的证书名和私钥名，并将`channel_node_cert`配置为SDK证书路径，将`channel_node_key`配置为SDK私钥路径

检查从节点拷贝的sdk证书路径，若sdk证书和私钥路径分别为`bin/sdk.crt`和`bin/sdk.key`，则`client_config.py`中相关配置项如下：

```bash
channel_node_cert = "bin/sdk.crt"  # 采用channel协议时，需要设置sdk证书,如采用rpc协议通信，这里可以留空
channel_node_key = "bin/sdk.key"   # 采用channel协议时，需要设置sdk私钥,如采用rpc协议通信，这里可以留空
```

若sdk证书和私钥路径分别为`bin/node.crt`和`bin/node.key`，则`client_config.py`中相关配置项如下:
```bash
channel_node_cert = "bin/node.crt"  # 采用channel协议时，需要设置sdk证书,如采用rpc协议通信，这里可以留空
channel_node_key = "bin/node.key"   # 采用channel协议时，需要设置sdk私钥,如采用rpc协议通信，这里可以留空
```

**使用Channel协议访问节点**

```bash
# 获取FISCO BCOS节点版本号
./console.py getNodeVersion
```

## SDK使用示例

**查看SDK使用方法**

> **windows环境下执行console.py请使用`.\console.py`或者`python console.py`**

```bash
# 查看SDK使用方法
./console.py usage

# 获取节点版本
./console.py getNodeVersion
```

**部署HelloWorld合约**
```bash
$ ./console.py deploy HelloWorld save 

INFO >> user input : ['deploy', 'HelloWorld', 'save']

backup [contracts/HelloWorld.abi] to [contracts/HelloWorld.abi.20190807102912]
backup [contracts/HelloWorld.bin] to [contracts/HelloWorld.bin.20190807102912]
INFO >> compile with solc compiler
deploy result  for [HelloWorld] is:
 {
    "blockHash": "0x3912605dde5f7358fee40a85a8b97ba6493848eae7766a8c317beecafb2e279d",
    "blockNumber": "0x1",
    "contractAddress": "0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce",
    "from": "0x95198b93705e394a916579e048c8a32ddfb900f7",
    "gasUsed": "0x44ab3",
    "input": "0x6080604052...省略若干行...c6f2c20576f726c642100000000000000000000000000",
    "logs": [],
    "logsBloom": "0x000...省略若干行...0000",
    "output": "0x",
    "status": "0x0",
    "to": "0x0000000000000000000000000000000000000000",
    "transactionHash": "0xb291e9ca38b53c897340256b851764fa68a86f2a53cb14b2ecdcc332e850bb91",
    "transactionIndex": "0x0"
}
on block : 1,address: 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce 
address save to file:  bin/contract.ini
```

**调用HelloWorld合约**

```bash
# 合约地址：0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce
# 调用接口：get
$./console.py  call HelloWorld 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce get 

INFO >> user input : ['call', 'HelloWorld', '0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce', 'get']

INFO >> call HelloWorld , address: 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce, func: get, args:[]
INFO >> call result: ('Hello, World!',)

# 合约名：HelloWorld
# 合约地址：0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce
# 调用接口：set
# 参数："Hello, FISCO"
$ ./console.py sendtx HelloWorld 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce set "Hello, FISCO"

INFO >> user input : ['sendtx', 'HelloWorld', '0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce', 'set', 'Hello, FISCO']

INFO >> sendtx HelloWorld , address: 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce, func: set, args:['Hello, FISCO']

INFO >>  receipt logs : 
INFO >> transaction hash :  0xc20cbc6b0f28ad8fe1c560c8ce28c0e7eb7719a4a618a81604ac87ac46cc60f0
tx input data detail:
 {'name': 'set', 'args': ('Hello, FISCO',), 'signature': 'set(string)'}
receipt output : ()

# 调用get接口获取更新后字符串
$./console.py call HelloWorld 0x2d1c577e41809453c50e7e5c3f57d06f3cdd90ce get

INFO >> user input : ['call', 'HelloWorld', '0x42883e01ac97a3a5ef8a70c290abe0f67913964e', 'get']

INFO >> call HelloWorld , address: 0x42883e01ac97a3a5ef8a70c290abe0f67913964e, func: get, args:[]
INFO >> call result:  'Hello, FISCO!'
```

## 开启命令行自动补全

Python SDK引入[argcomplete](https://argcomplete.readthedocs.io/en/latest/)支持命令行补全，运行如下命令开启此功能(**bashrc仅需设置一次，设置之后每次登陆自动生效**)，**目前仅支持bash，不支持zsh**：

```bash
echo "eval \"\$(register-python-argcomplete ./console.py)\"" >> ~/.bashrc
source ~/.bashrc
```

## 文档

[**中文**](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/python_sdk/index.html)

## 贡献代码

- 我们欢迎并非常感谢您的贡献，请参阅[代码贡献流程](https://mp.weixin.qq.com/s/hEn2rxqnqp0dF6OKH6Ua-A
)。
- 如项目对您有帮助，欢迎star支持！
- 如果发现代码存在安全漏洞，请在[这里](https://security.webank.com)上报。


## 加入社区

**FISCO BCOS开源社区**是国内活跃的开源社区，社区长期为机构和个人开发者提供各类支持与帮助。已有来自各行业的数千名技术爱好者在研究和使用FISCO BCOS。如您对FISCO BCOS开源技术及应用感兴趣，欢迎加入社区获得更多支持与帮助。

![](https://media.githubusercontent.com/media/FISCO-BCOS/LargeFiles/master/images/QR_image.png)

## License
![license](https://img.shields.io/github/license/FISCO-BCOS/python-sdk.svg)

Python SDK的开源协议为[MIT License](https://opensource.org/licenses/MIT). 详情参考[LICENSE](./LICENSE)。
