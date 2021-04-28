from hedera import Hbar, FileCreateTransaction
from get_client import client, OPERATOR_KEY

fileContents = "Hedera hashgraph SDK in python is great! 好 👍"
tran = FileCreateTransaction()
resp = tran.setKeys(OPERATOR_KEY.getPublicKey()).setContents(fileContents).setMaxTransactionFee(Hbar(2)).execute(client)
print("nodeId: ",  resp.nodeId.toString())
receipt = resp.getReceipt(client)
fileId = receipt.fileId
print("file: ",  fileId.toString())
