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
    TokenBurnTransaction,
    TokenGrantKycTransaction,
    TokenWipeTransaction,
    TokenMintTransaction,
    TokenDeleteTransaction,
    TokenId,
    TokenType,
    )
from jnius import autoclass
from get_client import client, OPERATOR_ID, OPERATOR_KEY

ArrayList = autoclass("java.util.ArrayList")

tokenId = TokenId.fromString(sys.argv[1])
serial = int(sys.argv[2])

txn = TokenBurnTransaction().setTokenId(tokenId)
txn.addSerial(serial)
resp = txn.execute(client)
receipt = resp.getReceipt(client)

print(receipt.serials.toString())
