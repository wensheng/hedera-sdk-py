import os
import time
from itertools import count

from hedera import (
    AccountId,
    PrivateKey,
    Client,
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
    )

assert "OPERATOR_ID" in os.environ
assert "OPERATOR_KEY" in os.environ

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "")

if HEDERA_NETWORK == "previewnet":
    client = Client.forPreviewnet()
elif HEDERA_NETWORK == "testnet":
    client = Client.forTestnet()
else:
    client = Client.fromConfigFile(CONFIG_FILE)

client.setOperator(OPERATOR_ID, OPERATOR_KEY)

tran = TopicCreateTransaction()
transactionResponse = tran.execute(client)
receipt = transactionResponse.getReceipt(client)
topicId = receipt.topicId
print("New topic created: ",  topicId.toString())
time.sleep(5)
query = TopicMessageQuery().setTopicId(topicId)
query.subscribe(client, PyConsumer())

for i in count():
    sbtran = TopicMessageSubmitTransaction()
    resp = sbtran.setTopicId(topicId).setMessage("Hello HCS! " + str(i)).execute(client)
    resp.getReceipt(client)
    # print("receipt: ", resp.getReceipt(client).toString())
    time.sleep(2.5)
