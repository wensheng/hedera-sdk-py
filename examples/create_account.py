from hedera import (
    Hbar,
    PrivateKey,
    AccountCreateTransaction,
    )
from get_client import client

# Generate a Ed25519 private, public key pair
newKey = PrivateKey.generate()
newPublicKey = newKey.getPublicKey()

print("private key = ", newKey.toString())
print("public key = ", newPublicKey.toString())

tran = AccountCreateTransaction()
# need a certain number of hbars, otherwise it can not be deleted later
resp = tran.setKey(newPublicKey).setInitialBalance(Hbar(2)).execute(client)
receipt = resp.getReceipt(client)
print("account = ",  receipt.accountId.toString())
