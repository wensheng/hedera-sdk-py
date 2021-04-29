from hedera import (
    Hbar,
    PrivateKey,
    AccountBalanceQuery,
    AccountCreateTransaction,
    TransferTransaction,
    Transaction,
    )
from get_client import client
from jnius import cast


exchangeKey = PrivateKey.generate()
userKey = PrivateKey.generate()
print("Exchange Key : ", exchangeKey.toString())
print("User Key : ", userKey.toString())

# the exchange only accepts transfers that it validates through a side channel (e.g. REST API)
# The owner key has to sign this transaction
# when setReceiverSignatureRequired is true
tran = AccountCreateTransaction(
       ).setInitialBalance(Hbar(1)
       ).setReceiverSignatureRequired(True
       ).setKey(exchangeKey
       ).freezeWith(client
       ).sign(exchangeKey)
receipt = tran.execute(client).getReceipt(client)
exchangeAccountId = receipt.accountId
print("exchange account = ",  exchangeAccountId.toString())

tran = AccountCreateTransaction().setInitialBalance(Hbar(5)).setKey(userKey)
receipt = tran.execute(client).getReceipt(client)
userAccountId = receipt.accountId
print("user account = ",  userAccountId.toString())

# the exchange-provided memo required to validate the transaction
# NOTE: to manually sign, you must freeze the Transaction first
transferTxn = TransferTransaction(
              ).addHbarTransfer(userAccountId, Hbar(2).negated()
              ).addHbarTransfer(exchangeAccountId, Hbar(2)
              ).setTransactionMemo("https://some-exchange.com/user1/account1"
              ).freezeWith(client
              ).sign(userKey)

# the exchange must sign the transaction in order for it to be accepted by the network
# assume this is some REST call to the exchange API server
signedTxnBytes = Transaction.fromBytes(transferTxn.toBytes()).sign(exchangeKey).toBytes()
# parse the transaction bytes returned from the exchange
signedTransferTxn = Transaction.fromBytes(signedTxnBytes)

# get the amount we are about to transfer
# we built this with +2, -2
realTransferTxn = cast(TransferTransaction, signedTransferTxn)
transferAmount = realTransferTxn.getHbarTransfers().values().toArray()[0].toString()
print("about to transfer ", transferAmount, "...")

# we now execute the signed transaction and wait for it to be accepted
transactionResponse = signedTransferTxn.execute(client)

# (important!) wait for consensus by querying for the receipt
transactionResponse.getReceipt(client)

senderBalanceAfter = AccountBalanceQuery().setAccountId(userAccountId).execute(client).hbars
receiptBalanceAfter = AccountBalanceQuery().setAccountId(exchangeAccountId).execute(client).hbars

print(userAccountId.toString(), " balance = ", senderBalanceAfter.toString())
print(exchangeAccountId.toString(), " balance = ", receiptBalanceAfter.toString())
