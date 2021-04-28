from hedera import (
    Hbar,
    FileId,
    FileContentsQuery,
    )
from get_client import client

query = FileContentsQuery().setFileId(FileId.ADDRESS_BOOK)
cost = query.getCost(client)
print("file contents cost: ", cost.toString())

query = query.setMaxQueryPayment(Hbar(1))
contents = query.execute(client)
with open("address-book.proto.bin", "wb") as f:
    f.write(bytes(contents.toByteArray().tolist()))
    print("address-book.proto.bin saved")
