import time
from hedera import (
    Hbar,
    AccountId,
    AccountBalanceQuery,
    TransferTransaction,
    )
from get_client import client, OPERATOR_ID

recipientId = AccountId.fromString("0.0.3")
amount = Hbar.fromTinybars(10_000_000)

senderBalanceBefore = AccountBalanceQuery().setAccountId(OPERATOR_ID).execute(client).hbars
recipientBalanceBefore = AccountBalanceQuery().setAccountId(recipientId).execute(client).hbars

print(OPERATOR_ID.toString(), " balance = ", senderBalanceBefore.toString())
print(recipientId.toString(), " balance = ", recipientBalanceBefore.toString())

resp = TransferTransaction(
       ).addHbarTransfer(OPERATOR_ID, amount.negated()
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
