"""
This example should be run after you create a new account, probably with create_account.py
you need to take notes of account_id and private_key after the account is created
"""

import sys
import time
from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    AccountInfoQuery,
    AccountDeleteTransaction,
    TransactionId,
    )
from get_client import client, OPERATOR_ID

if len(sys.argv) < 3:
    exit("Need a account id and private_key")

accountId = AccountId.fromString(sys.argv[1])
pri_key = PrivateKey.fromString(sys.argv[2])

query = AccountInfoQuery().setAccountId(accountId).setQueryPayment(Hbar(1))
try:
    resp = query.execute(client)
    print("account info before delete: ", resp.toString())
except Exception as e:
    exit("Failed: {}".format(e))

tran = AccountDeleteTransaction()
resp = tran.setAccountId(accountId
          ).setTransferAccountId(OPERATOR_ID
          ).setTransactionId(TransactionId.generate(accountId)
          ).freezeWith(client
          ).sign(pri_key
          ).execute(client)
receipt = resp.getReceipt(client)
print("account delete transaction executed: ", resp.transactionId.toString())

time.sleep(2)

query = AccountInfoQuery().setAccountId(accountId).setQueryPayment(Hbar(1))
try:
    resp = query.execute(client)
except Exception as e:
    print(e)
    print("status should be 'ACCOUNT_DELETED'")
