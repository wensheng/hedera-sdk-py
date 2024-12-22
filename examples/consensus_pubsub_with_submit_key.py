import os
import time
from random import randint

from hedera import (
    PrivateKey,
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
    )
from get_client import client
from jnius import autoclass

messagesToPublish = 5
secondsBetweenMessages = 2

# this need to be cleaned up
mirror_node_address = os.environ.get('MIRROR_NODE_ADDRESS', "hcs.testnet.mirrornode.hedera.com:5600")
JList = autoclass("java.util.List")
mirror_node = JList.of(mirror_node_address)
client.setMirrorNetwork(mirror_node)

# createTopicWithSubmitKey
submitKey = PrivateKey.generate()
submitPublicKey = submitKey.getPublicKey()

resp = (TopicCreateTransaction()
        .setTopicMemo("HCS topic with submit key")
        .setSubmitKey(submitPublicKey)
        .execute(client))

topicId = resp.getReceipt(client).topicId
print("Created new topic ", topicId.toString(), " with ED25519 submitKey of ", submitKey.toString())

time.sleep(5)


def showMsg(*args):
    # print("time: {} received topic message: {}".format(args[0], args[2]))
    msg = args[0]
    print("time: {} received topic message: {}".format(msg.timestamp, msg.contents))


# subscribeToTopic
# will not use this: .setStartTime(Instant.ofEpochSecond(0))
# Instant is org.threeten.bp backport, but hedera sdk already use at least java 8
query = (TopicMessageQuery()
         .setTopicId(topicId)
         .subscribe(client, PyConsumer(showMsg)))

time.sleep(2)

# publishMessagesToTopic
for i in range(messagesToPublish):
    message = "random message " + str(randint(0, 10 ** 9))
    print("Publishing message: ", message)

    # The transaction is automatically signed by the payer.
    # Due to the topic having a submitKey requirement, additionally sign the transaction with that key.
    receipt = (TopicMessageSubmitTransaction()
               .setTopicId(topicId)
               .setMessage(message)
               .freezeWith(client)
               .sign(submitKey)
               .execute(client)
               .transactionId.getReceipt(client))

    time.sleep(secondsBetweenMessages)

time.sleep(10)
