import os
from hedera import (
    AccountId,
    PrivateKey,
    Client,
    AccountBalanceQuery,
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

query = AccountBalanceQuery()
response = query.setAccountId(OPERATOR_ID).execute(client)
balance = response.hbars
print("balance = ",  balance.toString())
