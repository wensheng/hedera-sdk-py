import sys
from hedera import (
    TokenBurnTransaction,
    TokenId,
    )
from jnius import autoclass
from get_client import client

ArrayList = autoclass("java.util.ArrayList")

tokenId = TokenId.fromString(sys.argv[1])
serial = int(sys.argv[2])

txn = TokenBurnTransaction().setTokenId(tokenId)
txn.addSerial(serial)
resp = txn.execute(client)
receipt = resp.getReceipt(client)

print(receipt.serials.toString())
