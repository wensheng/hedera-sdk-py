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
    TokenType,
    )
from jnius import autoclass
from get_client import client, OPERATOR_ID, OPERATOR_KEY

Collections = autoclass("java.util.Collections")


nodeIds = Collections.singletonList(client.network.nodes.toArray()[0].accountId)
#txn = TokenCreateTransaction().setNodeAccountIds(nodeIds)
txn = (TokenCreateTransaction()
       .setNodeAccountIds(nodeIds)
       .setTokenName("MyNFT")
       .setTokenSymbol("MNFT")
       .setTokenType(TokenType.valueOf('NON_FUNGIBLE_UNIQUE'))
       .setTreasuryAccountId(OPERATOR_ID)
       .setAdminKey(OPERATOR_KEY.getPublicKey())
       .setFreezeKey(OPERATOR_KEY.getPublicKey())
       .setWipeKey(OPERATOR_KEY.getPublicKey())
       .setKycKey(OPERATOR_KEY.getPublicKey())
       .setSupplyKey(OPERATOR_KEY.getPublicKey())
       .setFreezeDefault(False)
       .execute(client))

tokenId = txn.getReceipt(client).tokenId
print("token = ", tokenId.toString())
