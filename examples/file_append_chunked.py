import os
import sys
from hedera import (
    Hbar,
    FileId,
    FileAppendTransaction,
    FileInfoQuery,
    )
from get_client import client

if len(sys.argv) < 2:
    exit("need fileId")

fileId = FileId.fromString(sys.argv[1])

cur_dir = os.path.abspath(os.path.dirname(__file__))
fr = open(os.path.join(cur_dir, "large_message.txt"))
fileContents = fr.read()  # 13494 bytes
fr.close()

# this used to work with 1024 * 36
#fileContents = "%s%s" % (fileContents, "I" * (1024 * 10))
# the default TransactionValidDuration is 120s
# to get it to work with bigger message, we need to setTransactionValidDuration
# which use org.threeten.bp.Duration, which I don't want to use


print("This will take a while, 1-2 min.")  # about 1 and half minute
tran = (FileAppendTransaction()
        .setFileId(fileId)
        .setContents(fileContents)
        .setMaxChunks(15)
        .setMaxTransactionFee(Hbar(1000))
        .freezeWith(client))
resp = tran.execute(client)
receipt = resp.getReceipt(client)

print(receipt.toString())

query = FileInfoQuery().setFileId(fileId)
info = query.execute(client)
print("File size according to `FileInfoQuery`: ", info.size)
