from hedera import AccountBalanceQuery
from get_client import client, OPERATOR_ID

balance = AccountBalanceQuery().setAccountId(OPERATOR_ID).execute(client)
print("Hbar balance = ",  balance.hbars.toString())
tokens = balance.tokens
for tokenId in tokens.keySet().toArray():
    print("Token {} = {}".format(tokenId.toString(), tokens[tokenId]))
