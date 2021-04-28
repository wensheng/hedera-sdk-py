from hedera import AccountBalanceQuery
from get_client import client, OPERATOR_ID

balance = AccountBalanceQuery().setAccountId(OPERATOR_ID).execute(client).hbars
print("balance = ",  balance.toString())
