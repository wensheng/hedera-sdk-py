import sys
from hedera import FileId, FileContentsQuery
from get_client import client

if len(sys.argv) < 2:
    exit("need a file id")

fileId = FileId.fromString(sys.argv[1])
query = FileContentsQuery()
contents = query.setFileId(fileId).execute(client)
print("File content query results: ",  contents.toStringUtf8())
