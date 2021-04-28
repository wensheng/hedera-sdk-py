import time
from itertools import count

from hedera import (
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
    )
from get_client import client

tran = TopicCreateTransaction()
transactionResponse = tran.execute(client)
receipt = transactionResponse.getReceipt(client)
topicId = receipt.topicId
print("New topic created: ",  topicId.toString())
time.sleep(5)
query = TopicMessageQuery().setTopicId(topicId)


def showMessage(*args):
    print("time: {} received: {}".format(args[0], args[2]))


query.subscribe(client, PyConsumer(showMessage))

for i in count():
    sbtran = TopicMessageSubmitTransaction()
    resp = sbtran.setTopicId(topicId).setMessage("Hello HCS! " + str(i)).execute(client)
    resp.getReceipt(client)
    # print("receipt: ", resp.getReceipt(client).toString())
    time.sleep(2.5)
