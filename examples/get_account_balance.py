from hedera import AccountBalanceQuery
from get_client import client, OPERATOR_ID

query = AccountBalanceQuery()
response = query.setAccountId(OPERATOR_ID).execute(client)
balance = response.hbars
print("balance = ",  balance.toString())
