import sys
from hedera import (
    TokenMintTransaction,
    TokenId,
    )
from jnius import autoclass
from get_client import client

ArrayList = autoclass("java.util.ArrayList")

tokenId = TokenId.fromString(sys.argv[1])
amount = int(sys.argv[2])

if amount > 10:
    exit("Can not mint more than 10 nft's")

#meta = ArrayList()
#for i in range(amount):
#    meta.add(f'https://example.com/token/metadata/{i}'.encode())
## .setAmount(n) doesn't apply to NFT
#try:
##           .setAmount(amount)
#    txn = (TokenMintTransaction()
#           .setTokenId(tokenId)
#           .setMetadata(meta))
#    resp = txn.execute(client)
#    receipt = resp.getReceipt(client)
#except Exception as e:
#    print(e)

txn = TokenMintTransaction().setTokenId(tokenId)
for i in range(amount):
    txn.addMetadata(f'https://thisksdjfkdsjfksdjfkjdskfjsdkjfksdjfksdjfkdsjkfjsaaaakfjkdsjfkdsexample.com/token/metadata/{i}'.encode())
resp = txn.execute(client)
receipt = resp.getReceipt(client)

print(receipt.serials.toString())
