"""
as of 2021/4 this is not supported on testnet, use previewnet to run this exeample
"""
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    KeyList,
    TransactionId,
    ScheduleInfoQuery,
    ScheduleSignTransaction,
    AccountCreateTransaction,
    TransferTransaction,
    )
from get_client import client, OPERATOR_ID
from jnius import autoclass, cast

JCollections = autoclass('java.util.Collections')

key1 = PrivateKey.generate()
key2 = PrivateKey.generate()
key3 = PrivateKey.generate()
pkey1 = key1.getPublicKey()
pkey2 = key2.getPublicKey()
pkey3 = key3.getPublicKey()
keyList = KeyList.of(pkey1, pkey2, pkey3)

print("key1 private = ", key1.toString())
print("key1 public = ", pkey1.toString())
print("key2 private = ", key2.toString())
print("key2 public = ", pkey2.toString())
print("key3 private = ", key3.toString())
print("key3 public = ", pkey3.toString())

resp = AccountCreateTransaction(
       ).setNodeAccountIds(JCollections.singletonList(AccountId(3))
       ).setKey(keyList
       ).setInitialBalance(Hbar(10)
       ).execute(client)

nodeId = resp.nodeId
accountId = resp.getReceipt(client).accountId
print("accountId = ",  accountId.toString())


# Generate a `TransactionId`. This id is used to query the inner scheduled transaction
# after we expect it to have been executed
transactionId = TransactionId.generate(OPERATOR_ID)
print("transactionId for scheduled transaction = ", transactionId.toString())

# Create a transfer transaction with 2/3 signatures.
transfer = TransferTransaction(
           ).addHbarTransfer(accountId, Hbar(1).negated()
           ).addHbarTransfer(OPERATOR_ID, Hbar(1))

# Schedule the transactoin
scheduled = transfer.schedule(
            ).setPayerAccountId(client.getOperatorAccountId()
            ).setAdminKey(client.getOperatorPublicKey()
            ).freezeWith(client
            ).sign(key2)

# Get the schedule ID from the receipt
scheduleId = scheduled.execute(client).getReceipt(client).scheduleId
print("scheduleId = ", scheduleId.toString())

# Get the schedule info to see if `signatories` is populated with 2/3 signatures
info = ScheduleInfoQuery(
       ).setNodeAccountIds(JCollections.singletonList(nodeId)
       ).setScheduleId(scheduleId
       ).execute(client)

print("Schedule Info = ", info.toString())

# Make sure the transfer transaction is what we expect
transfer = cast(TransferTransaction, info.getScheduledTransaction())
transfers = transfer.getHbarTransfers()
if transfers.size() != 2:
    exit("more transfers than expected")

if not transfers.get(accountId) == Hbar(1).negated():
    exit("transfer for " + accountId.toString() + " is not what is expected " + transfers.get(accountId).toString())

if not transfers.get(OPERATOR_ID) == Hbar(1):
    exit("transfer for " + OPERATOR_ID.toString() + " is not what is expected " + transfers.get(OPERATOR_ID).toString())

print("sending schedule sign transaction")

# Finally send this last signature to Hedera. This last signature _should_ mean the transaction executes
# since all 3 signatures have been provided.
receipt = ScheduleSignTransaction(
          ).setNodeAccountIds(JCollections.singletonList(nodeId)
          ).setScheduleId(scheduleId
          ).freezeWith(client
          ).sign(key3
          ).execute(client
          ).getReceipt(client)

# Query the schedule info again
result = ScheduleInfoQuery(
         ).setNodeAccountIds(JCollections.singletonList(nodeId)
         ).setScheduleId(scheduleId
         ).execute(client)

print(result.toString())
