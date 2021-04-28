import os
import time
import json

from hedera import (
    Hbar,
    FileCreateTransaction,
    ContractCreateTransaction,
    ContractCallQuery,
    ContractDeleteTransaction,
    )
from get_client import client, OPERATOR_KEY

cur_dir = os.path.abspath(os.path.dirname(__file__))
jsonf = open(os.path.join(cur_dir, "hello_world.json"))
hello_world = json.load(jsonf)

tran = FileCreateTransaction()
resp = tran.setKeys(OPERATOR_KEY
       ).setContents(hello_world['object'].encode()
       ).setMaxTransactionFee(Hbar(2)
       ).execute(client)
receipt = resp.getReceipt(client)
fileId = receipt.fileId

print("contract bytecode file: ", fileId.toString())

tran = ContractCreateTransaction()
resp = tran.setGas(500
       ).setBytecodeFileId(fileId
       ).setAdminKey(OPERATOR_KEY
       ).setMaxTransactionFee(Hbar(16)
       ).execute(client)
receipt = resp.getReceipt(client)
contractId = receipt.contractId
print(receipt.toString())
print("new contract id: ", contractId.toString())

query = ContractCallQuery()
result = query.setGas(600
         ).setContractId(contractId
         ).setFunction("greet"
         ).setMaxQueryPayment(Hbar(1)
         ).execute(client)

if result.errorMessage:
    exit("error calling contract: ", result.errorMessage)

message = result.getString(0)
print("contract message: ", message)

print("deleting contract in 10 seconds")
time.sleep(10)

tran = ContractDeleteTransaction()
resp = tran.setContractId(contractId
       ).setMaxTransactionFee(Hbar(1)
       ).execute(client)
receipt = resp.getReceipt(client)
print("Deleting contract - status: ", receipt.status.toString())
