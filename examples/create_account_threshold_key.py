import time
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    KeyList,
    AccountCreateTransaction,
    TransferTransaction,
    AccountBalanceQuery,
    )
from get_client import client

keys = []
# Generate 3 Ed25519 private, public key pair
for i in range(3):
    keys.append(PrivateKey.generate())

print("private keys:")
for k in keys:
    print(k.toString())

# require 2 of the 3 keys we generated to sign on anything modifying this account
transactionKey = KeyList.of(keys[0], keys[1])
tran = AccountCreateTransaction()
resp = tran.setKey(transactionKey).setInitialBalance(Hbar(10)).execute(client)
receipt = resp.getReceipt(client)
newAccountId = receipt.accountId
print("account = ",  newAccountId.toString())

result = AccountBalanceQuery().setAccountId(newAccountId).execute(client)
print("account balance before transfer: ", result.hbars.toString())

tran = TransferTransaction()

# To manually sign, you must explicitly build the Transaction
# we sign with 2 of the 3 keys
resp = tran.addHbarTransfer(newAccountId, Hbar(2).negated()
          ).addHbarTransfer(AccountId(3), Hbar(2)
          ).freezeWith(client
          ).sign(keys[0]
          ).sign(keys[1]
          ).execute(client)

# (important!) wait for the transfer to go to consensus
receipt = resp.getReceipt(client)

time.sleep(3)
result = AccountBalanceQuery().setAccountId(newAccountId).execute(client)
print("account balance after transfer: ", result.hbars.toString())
