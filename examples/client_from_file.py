import os
from hedera import (
    Client,
    Hbar,
    PrivateKey,
    AccountCreateTransaction,
    )

cur_dir = os.path.abspath(os.path.dirname(__file__))

config_file = os.path.join(cur_dir, "client-config-with-operator.json")
client = Client.fromConfigFile(config_file)
newKey = PrivateKey.generate()
newPublicKey = newKey.getPublicKey()

resp = (AccountCreateTransaction()
        .setKey(newPublicKey)
        .setInitialBalance(Hbar.fromTinybars(1000))
        .execute(client))

receipt = resp.getReceipt(client)
print("account 1 = ",  receipt.accountId.toString())

config_file = os.path.join(cur_dir, "client-config.json")
client = Client.fromConfigFile(config_file)
newKey = PrivateKey.generate()
newPublicKey = newKey.getPublicKey()

resp = (AccountCreateTransaction()
        .setKey(newPublicKey)
        .setInitialBalance(Hbar.fromTinybars(1000))
        .execute(client))
receipt = resp.getReceipt(client)
print("account 2 = ",  receipt.accountId.toString())
