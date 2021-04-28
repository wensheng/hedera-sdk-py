import os
import json

from hedera import (
    Hbar,
    FileCreateTransaction,
    ContractCreateTransaction,
    ContractCallQuery,
    ContractExecuteTransaction,
    ContractFunctionParameters,
    )
from get_client import client, OPERATOR_KEY

client.setMaxTransactionFee(Hbar(100))
client.setMaxQueryPayment(Hbar(10))

cur_dir = os.path.abspath(os.path.dirname(__file__))
jsonf = open(os.path.join(cur_dir, "stateful.json"))
stateful_json = json.load(jsonf)
jsonf.close()
byteCode = stateful_json['object'].encode()

tran = FileCreateTransaction()
resp = tran.setKeys(OPERATOR_KEY
       ).setContents(byteCode
       ).execute(client)
fileId = resp.getReceipt(client).fileId
print("contract bytecode file: ", fileId.toString())

tran = ContractCreateTransaction()
resp = tran.setGas(100_000_000
       ).setBytecodeFileId(fileId
       ).setConstructorParameters(
               ContractFunctionParameters().addString("hello from hedera!")
       ).execute(client)
contractId = resp.getReceipt(client).contractId
print("new contract id: ", contractId.toString())

# 600 < gas fee < 1000
result = ContractCallQuery(
         ).setGas(1000
         ).setContractId(contractId
         ).setFunction("get_message"
         ).execute(client)

if result.errorMessage:
    exit("error calling contract: ", result.errorMessage)

message = result.getString(0)
print("contract returned message: ", message)

resp = ContractExecuteTransaction(
       ).setGas(100_000_000
       ).setContractId(contractId
       ).setFunction("set_message",
           ContractFunctionParameters().addString("hello from hedera again!")
       ).execute(client)

# if this doesn't throw then we know the contract executed successfully
receipt = resp.getReceipt(client)

# now query contract
result = ContractCallQuery(
         ).setGas(100_000_000
         ).setContractId(contractId
         ).setFunction("get_message"
         ).execute(client)

if result.errorMessage:
    exit("error calling contract: ", result.errorMessage)

message = result.getString(0)
print("contract returned message: ", message)
