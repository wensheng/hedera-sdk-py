import sys
from hedera import FileId, FileDeleteTransaction
from get_client import client

if len(sys.argv) < 2:
    exit("need a file id")

fileId = FileId.fromString(sys.argv[1])
tran = FileDeleteTransaction()
resp = tran.setFileId(fileId).execute(client)
receipt = resp.getReceipt(client)
print("file deleted successfully")
