import time
from itertools import count
from hedera import (
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
    )
from get_client import client


def showMessage(*args):
    print("time: {} received: {}".format(args[0], args[2]))


resp = TopicCreateTransaction().execute(client)
topicId = resp.getReceipt(client).topicId
print("New topic created: ",  topicId.toString())
time.sleep(5)

# It's recommended to use another seperate program to subscribe to topic
# please see https://github.com/wensheng/hcs-grpc-api-py-client for using grpc client
query = TopicMessageQuery().setTopicId(topicId)
query.subscribe(client, PyConsumer(showMessage))

for i in count():
    tran = TopicMessageSubmitTransaction().setTopicId(topicId).setMessage(
            "Hello HCS! " + str(i))
    tran.execute(client).getReceipt(client)
    time.sleep(2.5)
