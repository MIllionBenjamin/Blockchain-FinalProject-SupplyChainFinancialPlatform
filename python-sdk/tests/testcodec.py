'''
  @author: kentzhang
  @date: 2019-06
'''
from eth_abi import encode_single, encode_abi,decode_single
from eth_utils import *
import json
#print (encode_single('uint256', 12345) )

abitext='(uint256,uint256)'
data = encode_single(abitext, [8899,765])
#print (decode_single(abitext,data))
#print (encode_hex(data))
text = ""

def testjson():
    with open("AddrTableWorker.abi",'r') as load_f:
        load_dict = json.load(load_f)
        for item in load_dict:
            if(item["type"] != "constructor"):
                print(item["name"]," is a " , item["type"])
                hash4 = function_signature_to_4byte_selector(item["name"] + '()')
                print("function hash4:" , encode_hex(hash4) )



    with open("abi_1.json","w") as dump_f:
        json.dump(load_dict,dump_f)

testjson()

logtext = '''
{    "logs":[
        {
            "address":"0x7029c502b4f824d19bd7921e9cb74ef92392fb1b",
            "data":"0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000000036162630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f6e616d6520657869737473202c63616e27742063726561746520616761696e00",
            "topics":[
                "0xcb49392692818ccbce107b9d246d4729b350f32844060c37634542a16378a860"
            ]
        }
        ]
}
'''
logdict = json.loads(logtext)
data = logdict["logs"][0]["data"];
print(logdict["logs"][0]["topics"])
from eth_utils import keccak

eventname = "createEvent(int256 ret, string name, uint256 balance, address city, string memo)"
from eth_utils.curried import hexstr_if_str
eventABI = '''{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "ret",
				"type": "int256"
			},
			{
				"indexed": false,
				"name": "name",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "balance",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "city",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "memo",
				"type": "string"
			}
		],
		"name": "createEvent",
		"type": "event"
	}'''

jsonobj =json.loads(eventABI);
print(jsonobj)




topicbytes= event_abi_to_log_topic(json.loads(eventABI))
print(encode_hex(topicbytes) )
data = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000000036162630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001f6e616d6520657869737473202c63616e27742063726561746520616761696e00"
result = decode_single("(int256,string,uint256,address,string)",decode_hex(data) )
print(result)




