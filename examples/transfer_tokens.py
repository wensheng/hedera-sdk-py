import time
from hedera import (
    Hbar,
    PrivateKey,
    AccountCreateTransaction,
    AccountDeleteTransaction,
    TransferTransaction,
    TokenCreateTransaction,
    TokenAssociateTransaction,
    TokenGrantKycTransaction,
    TokenWipeTransaction,
    TokenDeleteTransaction,
    )
from jnius import autoclass
from get_client import client, OPERATOR_ID, OPERATOR_KEY

Collections = autoclass("java.util.Collections")


key1 = PrivateKey.generate()
key2 = PrivateKey.generate()
print("Private Key 1: ", key1.toString())
print("Public Key 1: ", key1.getPublicKey().toString())
print("Private Key 2: ", key2.toString())
print("Public Key 2: ", key2.getPublicKey().toString())

resp = AccountCreateTransaction(
       ).setKey(key1.getPublicKey()
       ).setInitialBalance(Hbar(1)
       ).execute(client)
nodeId = resp.nodeId
accountId1 = resp.getReceipt(client).accountId
print("account 1 = ",  accountId1.toString())

resp = AccountCreateTransaction(
       ).setKey(key2.getPublicKey()
       ).setInitialBalance(Hbar(1)
       ).execute(client)
accountId2 = resp.getReceipt(client).accountId
print("account 2 = ",  accountId2.toString())

resp = TokenCreateTransaction(
        ).setNodeAccountIds(Collections.singletonList(nodeId)
        ).setTokenName("ffff"
        ).setTokenSymbol("F"
        ).setDecimals(3
        ).setInitialSupply(1000000
        ).setTreasuryAccountId(OPERATOR_ID
        ).setAdminKey(OPERATOR_KEY.getPublicKey()
        ).setFreezeKey(OPERATOR_KEY.getPublicKey()
        ).setWipeKey(OPERATOR_KEY.getPublicKey()
        ).setKycKey(OPERATOR_KEY.getPublicKey()
        ).setSupplyKey(OPERATOR_KEY.getPublicKey()
        ).setFreezeDefault(False
        ).execute(client)

tokenId = resp.getReceipt(client).tokenId
print("token = ", tokenId.toString())

resp = TokenAssociateTransaction(
        ).setNodeAccountIds(Collections.singletonList(nodeId)
        ).setAccountId(accountId1
        ).setTokenIds(Collections.singletonList(tokenId)
        ).freezeWith(client
        ).sign(OPERATOR_KEY
        ).sign(key1
        ).execute(client)

receipt = resp.getReceipt(client)
print("Associated account ", accountId1.toString() + " with token " + tokenId.toString())

resp = TokenAssociateTransaction(
        ).setNodeAccountIds(Collections.singletonList(nodeId)
        ).setAccountId(accountId2
        ).setTokenIds(Collections.singletonList(tokenId)
        ).freezeWith(client
        ).sign(OPERATOR_KEY
        ).sign(key2
        ).execute(client)

receipt = resp.getReceipt(client)
print("Associated account ", accountId2.toString() + " with token " + tokenId.toString())


receipt = TokenGrantKycTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).setAccountId(accountId1
          ).setTokenId(tokenId
          ).execute(client
          ).getReceipt(client)

print("Granted KYC for account ", accountId1.toString(), " on token ", tokenId.toString())

receipt = TokenGrantKycTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).setAccountId(accountId2
          ).setTokenId(tokenId
          ).execute(client
          ).getReceipt(client)

print("Granted KYC for account ", accountId2.toString(), " on token ", tokenId.toString())

# operator -> account 1
receipt = TransferTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).addTokenTransfer(tokenId, OPERATOR_ID, -10
          ).addTokenTransfer(tokenId, accountId1, 10
          ).execute(client
          ).getReceipt(client)

print("Sent 10 tokens from account ", OPERATOR_ID.toString(),
      " to account ", accountId1.toString(), " on token ", tokenId.toString())

# account 1 -> account 2
receipt = TransferTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).addTokenTransfer(tokenId, accountId1, -10
          ).addTokenTransfer(tokenId, accountId2, 10
          ).freezeWith(client
          ).sign(key1
          ).execute(client
          ).getReceipt(client)

print("Sent 10 tokens from account ", accountId1.toString(),
      " to account ", accountId2.toString(), " on token ", tokenId.toString())

receipt = TransferTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).addTokenTransfer(tokenId, accountId2, -10
          ).addTokenTransfer(tokenId, accountId1, 10
          ).freezeWith(client
          ).sign(key2
          ).execute(client
          ).getReceipt(client)

print("Sent 10 tokens from account ", accountId2.toString(),
      " to account ", accountId1.toString(), " on token ", tokenId.toString())

receipt = TokenWipeTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).setTokenId(tokenId
          ).setAccountId(accountId1
          ).setAmount(10
          ).execute(client
          ).getReceipt(client)

print("Wiped balance of account ", accountId1.toString())

receipt = TokenDeleteTransaction(
          ).setNodeAccountIds(Collections.singletonList(nodeId)
          ).setTokenId(tokenId
          ).execute(client
          ).getReceipt(client)

print("Deleted token ", tokenId.toString())

receipt = AccountDeleteTransaction(
          ).setAccountId(accountId1
          ).setTransferAccountId(OPERATOR_ID
          ).freezeWith(client
          ).sign(OPERATOR_KEY
          ).sign(key1
          ).execute(client
          ).getReceipt(client)

print("Deleted accountId1 ", accountId1.toString())

receipt = AccountDeleteTransaction(
          ).setAccountId(accountId2
          ).setTransferAccountId(OPERATOR_ID
          ).freezeWith(client
          ).sign(OPERATOR_KEY
          ).sign(key2
          ).execute(client
          ).getReceipt(client)

print("Deleted accountId2", accountId2.toString())
# at least use the unneccessary variable `receipt` once
print("receipt status: ", receipt.status.toString())
