import os
import time
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    Client,
    AccountBalanceQuery,
    TransferTransaction,
    )

assert "OPERATOR_ID" in os.environ
assert "OPERATOR_KEY" in os.environ

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "")

# sending 1 hbar so make sure we don't use mainnet
assert HEDERA_NETWORK in ("testnet", "previewnet")

if HEDERA_NETWORK == "previewnet":
    client = Client.forPreviewnet()
elif HEDERA_NETWORK == "testnet":
    client = Client.forTestnet()
else:
    client = Client.fromConfigFile(CONFIG_FILE)

client.setOperator(OPERATOR_ID, OPERATOR_KEY)

recipientId = AccountId.fromString("0.0.3")
amount = Hbar.fromTinybars(100_000_000)

senderBalanceBefore = AccountBalanceQuery().setAccountId(OPERATOR_ID).execute(client).hbars
recipientBalanceBefore = AccountBalanceQuery().setAccountId(recipientId).execute(client).hbars

print(OPERATOR_ID.toString(), " balance = ", senderBalanceBefore.toString())
print(recipientId.toString(), " balance = ", recipientBalanceBefore.toString())


tran = TransferTransaction()
resp = tran.addHbarTransfer(OPERATOR_ID, amount.negated()
          ).addHbarTransfer(recipientId, amount
          ).setTransactionMemo("transfer test"
          ).execute(client)

print("transaction ID: ",  resp.toString())
print("transferred: ",  amount.toString())

time.sleep(2)  # need this to see balance change

senderBalanceAfter = AccountBalanceQuery().setAccountId(OPERATOR_ID).execute(client).hbars
recipientBalanceAfter = AccountBalanceQuery().setAccountId(recipientId).execute(client).hbars

print(OPERATOR_ID.toString(), " balance = ", senderBalanceAfter.toString())
print(recipientId.toString(), " balance = ", recipientBalanceAfter.toString())
record = resp.getRecord(client)
print("Transfer memo: ", record.transactionMemo)
