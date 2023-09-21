import sys
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
    TokenMintTransaction,
    TokenDeleteTransaction,
    TokenId,
    TokenType,
    )
from jnius import autoclass
from get_client import client, OPERATOR_ID, OPERATOR_KEY

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
