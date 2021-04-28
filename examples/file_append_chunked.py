import os
import sys
from hedera import (
    Hbar,
    AccountId,
    FileId,
    FileAppendTransaction,
    FileInfoQuery,
    )
from get_client import client
from jnius import autoclass

Collections = autoclass('java.util.Collections')

if len(sys.argv) < 3:
    exit("need nodeId and fileId")

nodeId = AccountId.fromString(sys.argv[1])
fileId = FileId.fromString(sys.argv[2])

cur_dir = os.path.abspath(os.path.dirname(__file__))
fr = open(os.path.join(cur_dir, "large_message.txt"))
fileContents = fr.read()
fr.close()

fileContents = "%s%s" % (fileContents, "i" * (4096 * 9))

print("This will take a while")  # about 1 and half minute
tran = FileAppendTransaction(
        ).setNodeAccountIds(Collections.singletonList(nodeId)
        ).setFileId(fileId
        ).setContents(fileContents
        ).setMaxChunks(50
        ).setMaxTransactionFee(Hbar(1000)
        ).freezeWith(client)
resp = tran.execute(client)
receipt = resp.getReceipt(client)

print(receipt.toString())

query = FileInfoQuery().setFileId(fileId)
info = query.execute(client)
print("File size according to `FileInfoQuery`: ", info.size)
