import os
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    Client,
    AccountCreateTransaction,
    )

assert "OPERATOR_ID" in os.environ
assert "OPERATOR_KEY" in os.environ

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet");
CONFIG_FILE = os.environ.get("CONFIG_FILE", "");

if HEDERA_NETWORK == "previewnet":
    client = Client.forPreviewnet();
elif HEDERA_NETWORK == "testnet":
    client = Client.forTestnet();
else:
    client = Client.fromConfigFile(CONFIG_FILE);

client.setOperator(OPERATOR_ID, OPERATOR_KEY);

# Defaults the operator account ID and key such that all generated transactions will be paid for
# by this account and be signed by this key

# Generate a Ed25519 private, public key pair
newKey = PrivateKey.generate()
newPublicKey = newKey.getPublicKey()

print("private key = ", newKey.toString())
print("public key = ", newPublicKey.toString())

tran = AccountCreateTransaction()
transactionResponse = tran.setKey(newPublicKey).setInitialBalance(Hbar.fromTinybars(1000)).execute(client)
receipt = transactionResponse.getReceipt(client)
newAccountId = receipt.accountId
print("account = ",  newAccountId.toString())
