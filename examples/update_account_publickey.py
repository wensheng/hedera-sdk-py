from hedera import (
    Hbar,
    PrivateKey,
    AccountCreateTransaction,
    AccountUpdateTransaction,
    AccountInfoQuery,
    )
from get_client import client

client.setMaxTransactionFee(Hbar(10))

key1 = PrivateKey.generate()
key2 = PrivateKey.generate()
print("Private Key 1: ", key1.toString())
print("Private Key 2: ", key2.toString())

tran = AccountCreateTransaction()
# need a certain number of hbars, otherwise it can not be deleted later
resp = tran.setKey(key1.getPublicKey()).setInitialBalance(Hbar(1)).execute(client)
receipt = resp.getReceipt(client)
accountId = receipt.accountId
print("account = ",  accountId.toString())
print("key = ",  key1.getPublicKey().toString())

tran = AccountUpdateTransaction(
        ).setAccountId(accountId
        ).setKey(key2.getPublicKey()
        ).freezeWith(client
        ).sign(key1
        ).sign(key2)
resp = tran.execute(client)
print("transaction ID: ", resp.toString())

# (important!) wait for the transaction to complete by querying the receipt
receipt = resp.getReceipt(client)

print(" :: getAccount and check our current key")

info = AccountInfoQuery().setAccountId(accountId).execute(client)
print("key = ", info.key.toString())
