import os
import sys
from hedera import (
    AccountId,
    PrivateKey,
    Client,
    FileId,
    FileDeleteTransaction,
    )

assert "OPERATOR_ID" in os.environ
assert "OPERATOR_KEY" in os.environ

if len(sys.argv) < 2:
    exit("need a file id")

fileId = FileId.fromString(sys.argv[1])

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

tran = FileDeleteTransaction()
resp = tran.setFileId(fileId).execute(client)
receipt = resp.getReceipt(client)
print("file deleted successfully")
