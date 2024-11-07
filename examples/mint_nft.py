import sys
from hedera import (
    TokenMintTransaction,
    TokenId,
    )
from jnius import autoclass
from get_client import client

Collections = autoclass("java.util.Collections")
meta = "https://example.com/fake/address"

tokenId = TokenId.fromString(sys.argv[1])
# .setAmount(n) doesn't apply to NFT
try:
    txn = (TokenMintTransaction()
           .setTokenId(tokenId)
           .addMetadata(meta.encode())
           .execute(client))

    receipt = txn.getReceipt(client)
except Exception as e:
    print(e)
