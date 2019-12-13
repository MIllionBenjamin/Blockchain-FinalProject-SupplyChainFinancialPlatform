#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/FISCO-BCOS)
  bcosliteclientpy is free software: you can redistribute it and/or modify it
  under the terms of the MIT License as published by the Free Software Foundation
  This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
  Thanks for authors and contributors of eth-abi，eth-account，eth-hash，eth-keys，eth-typing，
  eth-utils，rlp, eth-rlp , hexbytes ...and relative projects
  @author: kentzhang
  @date: 2019-07
'''
import os
import sys
import platform

platsys = platform.system()
solc_bin = "bin/solc/solc"
solc_option = "--abi --bin --overwrite"
solc_default_output = "./contracts"

if platsys.lower().startswith("win"):
    solc_bin = solc_bin.replace("/", "\\")


# sample: bin/solc/solc.exe --abi --bin --allow-paths=./contracts contracts/Test.sol -o ./tmp
def sol_cmdline(solfile, outputpath, option=solc_option):
    solpath = os.path.dirname(solfile)
    allowpath = ""
    if solpath == "":
        allowpath = "--allow-paths=" + solpath
    cmdline = "{} {} {} -o {} {}".format(solc_bin, option, allowpath, outputpath, solfile)
    return cmdline


def run_cmd(cmdline):
    res = os.popen(cmdline).readlines()
    return res


def run_solc(solfile, outputpath, option=solc_option):
    cmdline = sol_cmdline(solfile, outputpath, option)
    print(cmdline)
    res = run_cmd(cmdline)
    if len(res) > 0:
        print(res)


solc_url_win = []
solc_url_win.append(
    ("v0.4   ",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.4.25/solc-windows.zip"))
solc_url_win.append(
    ("v0.4 gm",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.4.25/solc-gm-windows.exe"))
solc_url_win.append(
    ("v0.5   ",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.5.2/solc-windows.zip"))
solc_url_win.append(
    ("v0.5 gm",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.5.2/solc-gm-windows.exe"))
solc_url_linux = []
solc_url_linux.append(
    ("v0.4   ",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.4.25/solc-static-linux"))
solc_url_linux.append(
    ("v0.4 gm",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.4.25/solc-gm-static-linux"))
solc_url_linux.append(
    ("v0.5",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.5.2/solc-linux"))
solc_url_linux.append(
    ("v0.5 gm centos",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.5.2/solc-gm-centos"))
solc_url_linux.append(
    ("v0.5 gm ubuntu",
     "https://github.com/FISCO-BCOS/solidity/releases/download/v0.5.2/solc-gm-ubuntu"))


def print_solc_url():
    print("The OS platform is : [ {} ].".format(platsys))
    solc_url = solc_url_win
    if platsys.lower().startswith("win"):
        solc_url = solc_url_win
    else:
        solc_url = solc_url_linux
    i = 0
    for url in solc_url:
        i += 1
        print("{} ): {}  :  {}".format(i, url[0], url[1]))
    print("\n>>>TIPS:")
    print('''1. Download the solc binary according to your OS type (e.g. Linux/Windows) and solidity version.
2. Copy the solc binary to {python-sdk}/bin/solc/.
3. Make sure that the name of solc binary file is renamed to "solc",
or update the solc binary path constant in python-sdk/solcpy.py.''')


if __name__ == '__main__':
    # print (sys.argv)
    if(len(sys.argv) == 1):
        print("\nusage: python solc.py [contract file (with path)] [output dir]\n")
        print("** Read bin/solc/README.md , and download solc binary release first **\n")
        print_solc_url()
        sys.exit(0)

    solfile = sys.argv[1]
    outputdir = solc_default_output
    if (len(sys.argv) == 3):
        outputdir = sys.argv[2]
    print("compile [{}],output to [{}]".format(solfile, outputdir))
    run_solc(solfile, outputdir)
    name = os.path.splitext(os.path.basename(solfile))[0]
    outputbin = "{}/{}.bin".format(outputdir, name)
    outputabi = "{}/{}.abi".format(outputdir, name)
    print("** check the output  -> [{},{}]".format(outputbin, outputabi))
    size = os.path.getsize(outputbin)
    print("bin : [ {} ] file size: {}".format(outputbin, size))

    size = os.path.getsize(outputabi)
    print("abi : [ {} ] file size: {}".format(outputabi, size))
