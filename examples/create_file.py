import os
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    Client,
    FileCreateTransaction,
    )

assert "OPERATOR_ID" in os.environ
assert "OPERATOR_KEY" in os.environ

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "")

if HEDERA_NETWORK == "previewnet":
    client = Client.forPreviewnet()
elif HEDERA_NETWORK == "testnet":
    client = Client.forTestnet()
else:
    client = Client.fromConfigFile(CONFIG_FILE)

client.setOperator(OPERATOR_ID, OPERATOR_KEY)

fileContents = "Hedera hashgraph SDK in python is great!"

tran = FileCreateTransaction()
resp = tran.setKeys(OPERATOR_KEY.getPublicKey()).setContents(fileContents).setMaxTransactionFee(Hbar(2)).execute(client)
receipt = resp.getReceipt(client)
fileId = receipt.fileId
print("file: ",  fileId.toString())
