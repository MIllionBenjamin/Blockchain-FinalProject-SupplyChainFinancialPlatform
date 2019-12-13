'''
  @author: kentzhang
  @date: 2019-06
'''
from eth_account.account import (
    Account
)
from eth_utils.hexadecimal import decode_hex,encode_hex

ac1 = Account.create('123456')
print(ac1.address)
print(encode_hex(ac1.key) )
print(ac1.publickey)
print()

kf = Account.encrypt(ac1.privateKey,"123456")
print(kf)
import json
keyfile ="d:/blockchain/accounts/pyaccount.keystore"
with open(keyfile, "w") as dump_f:
    json.dump(kf, dump_f)

with open(keyfile, "r") as dump_f:
    keytext = json.load(dump_f)
    privkey = Account.decrypt(keytext,"123456")
    ac2 = Account.from_key(privkey)
    print("read from file:",ac2.address)
    print(encode_hex(ac2.key) )
    print(ac2.publickey)