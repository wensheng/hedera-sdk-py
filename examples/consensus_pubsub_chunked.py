import os
import time
from itertools import count

from hedera import (
    PrivateKey,
    Client,
    Transaction,
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
    )
from get_client import client

clientWithoutOperator = Client.forTestnet()
submitKey = PrivateKey.generate()

tran = TopicCreateTransaction(
       ).setTopicMemo("hedera-sdk-py/examples/consensus_pubsub_chunked"
       ).setSubmitKey(submitKey)
newTopicId = tran.execute(client).getReceipt(client).topicId
print("New topic created: ",  newTopicId.toString())
print("wait 10s to propagate to the mirror ...")
time.sleep(10)

query = TopicMessageQuery().setTopicId(newTopicId)

def show_msg(*args):
    print("time:", args[0], "seq#:", args[1], "content:", args[2])


query.subscribe(client, PyConsumer(show_msg))

cur_dir = os.path.abspath(os.path.dirname(__file__))
fr = open(os.path.join(cur_dir, "large_message.txt"))
bigContents = fr.read()
fr.close()

print("about to prepare a transaction to send a message of ", len(bigContents), " bytes")
# sign with the operator or "sender" of the message
# this is the party who will be charged the transaction fee
# MaxChunks was 5, but need 14
tran = TopicMessageSubmitTransaction(
       ).setTopicId(newTopicId
       ).setMessage(bigContents
       ).setMaxChunks(15
       ).signWithOperator(client)

# serialize to bytes so we can be signed "somewhere else" by the submit key
transactionBytes = tran.toBytes()

# now pretend we sent those bytes across the network
# parse them into a transaction so we can sign as the submit key
transaction = Transaction.fromBytes(transactionBytes)

# view out the message size from the parsed transaction
# this can be useful to display what we are about to sign
#transactionMessageSize = ((TopicMessageSubmitTransaction)transaction).getMessage().size()
#System.out.println("about to send a transaction with a message of " + transactionMessageSize + " bytes")

# sign with that submit key
transaction.sign(submitKey)

# now actually submit the transaction
# get the receipt to ensure there were no errors
transaction.execute(client).getReceipt(client)

for i in count():
    print("waiting ..., if message is received, press ctrl-c to exit")
    time.sleep(2.5)
