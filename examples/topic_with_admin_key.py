from hedera import (
    PrivateKey,
    KeyList,
    TopicCreateTransaction,
    TopicUpdateTransaction,
    TopicInfoQuery,
    )
from get_client import client

initialAdminKeys = [PrivateKey.generate() for i in range(3)]
thresholdKey = KeyList.of(initialAdminKeys[0], initialAdminKeys[1])

# Create topic
tran = TopicCreateTransaction(
       ).setTopicMemo("demo topic"
       ).setAdminKey(thresholdKey
       ).freezeWith(client
       ).sign(initialAdminKeys[0]
       ).sign(initialAdminKeys[1])

resp = tran.execute(client)
topicId = resp.getReceipt(client).topicId
print("Created new topic ", topicId.toString(), " with 2-of-3 threshold key as adminKey.")

newAdminKeys = [PrivateKey.generate() for i in range(4)]
thresholdKey = KeyList.of(newAdminKeys[0], newAdminKeys[1], newAdminKeys[2])

# Sign with the initial adminKey. 2 of the 3 keys already part of the topic's adminKey.
# Sign with the new adminKey. 3 of 4 keys already part of the topic's adminKey.
tran = TopicUpdateTransaction(
       ).setTopicId(topicId
       ).setTopicMemo("updated demo topic"
       ).setAdminKey(thresholdKey
       ).freezeWith(client
       ).sign(initialAdminKeys[0]
       ).sign(initialAdminKeys[1]
       ).sign(newAdminKeys[0]
       ).sign(newAdminKeys[1]
       ).sign(newAdminKeys[2])

resp = tran.execute(client)
receipt = resp.getReceipt(client)
print("Updated topic ", topicId.toString(), " with 3-of-4 threshold key as adminKey.")
topicInfo = TopicInfoQuery().setTopicId(topicId).execute(client)
print(topicInfo.toString())
