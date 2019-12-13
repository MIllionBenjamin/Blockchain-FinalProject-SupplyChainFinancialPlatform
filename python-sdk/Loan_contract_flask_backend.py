from Loan_contract_invoke import Loan_Contract

from flask import Flask, abort, request, jsonify




all_info_on_chain = {"bank_info": [], "company_info": {}, "receipt_info": []}
loan_contract = Loan_Contract(address="0x54d20fa542252fecdab429831489fd8fb31295a0")


def update_bank_info():
    all_info_on_chain["bank_info"].clear()
    for i in range(0, loan_contract.get_bank_num()["bankNum"]):
        bank_info = loan_contract.get_bank_info_by_index(i)
        all_info_on_chain["bank_info"].append(bank_info["bankName"])
        
        
def update_company_info():
    all_info_on_chain["company_info"].clear()
    for i in range(0, loan_contract.get_company_num()["companyNum"]):
        company_info = loan_contract.get_company_info_by_index(i)
        all_info_on_chain["company_info"][company_info["companyName"]] = company_info
        
        
def update_receipt_info():
    all_info_on_chain["receipt_info"].clear()
    for i in range(0, loan_contract.get_receipt_num()["receiptNum"]):
        receipt_info = loan_contract.get_receipt_info_by_index(i)
        all_info_on_chain["receipt_info"].append(receipt_info)


def init_all_info_on_chain():
    update_bank_info()
    update_company_info()
    update_receipt_info()


init_all_info_on_chain()

        
    

app = Flask(__name__)

@app.route('/get_company_inf/', methods=['GET'])
def get_company_inf():
    update_company_info()
    if not request.args or "cpName" not in request.args:
        return jsonify({'result': 'not found'})
    else:
        cpName = str(request.args["cpName"])
        if cpName in all_info_on_chain["company_info"].keys():
            return jsonify(all_info_on_chain["company_info"][cpName]) 
        else:
            return jsonify({'result': 'not found'})


@app.route('/get_receipt/', methods=['GET'])
def get_receipt():
    update_receipt_info()
    if not request.args or "cpName" not in request.args:
        return jsonify([{'result': 'not found'}])
    else:
        cpName = str(request.args["cpName"])
        all_relative_receipts = []

        for i in range(0, len(all_info_on_chain["receipt_info"])):
            receipt = all_info_on_chain["receipt_info"][i]
            if receipt["Name_A"] == cpName or receipt["Name_B"] == cpName:
                all_relative_receipts.append(receipt)

        if len(all_relative_receipts) > 0:
            return jsonify(all_relative_receipts) 
        else:
            return jsonify([{'result': 'not found'}])


@app.route('/get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany/', methods=['GET'])
def get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany():
    update_bank_info()
    update_company_info()
    if not request.args or "bName" not in request.args or "cpName" not in request.args:
        return jsonify([{'result': 'not found'}])
    else:
        bName = str(request.args["bName"])
        cpName = str(request.args["cpName"])
        
        if bName not in all_info_on_chain["bank_info"] or cpName not in all_info_on_chain["company_info"].keys():
            return jsonify([{'result': 'not found'}])

        return loan_contract.get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany(bName, cpName)



app.run(host="0.0.0.0", port=8383, debug=True)
loan_contract.exit()