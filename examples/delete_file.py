import sys
from hedera import FileId, FileDeleteTransaction
from get_client import client

if len(sys.argv) < 2:
    exit("need a file id")

fileId = FileId.fromString(sys.argv[1])
try:
    txn = (FileDeleteTransaction()
           .setFileId(fileId)
           .execute(client))
    receipt = txn.getReceipt(client)
    print("file deleted successfully.")
except Exception as e:
    print(e)

