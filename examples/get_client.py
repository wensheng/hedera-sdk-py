import os
import json
from dotenv import load_dotenv
from hedera import AccountId, PrivateKey, Client

load_dotenv()

if "HEDERA_CONFIG_FILE" in os.environ:
    client = Client.fromConfigFile(os.environ["HEDERA_CONFIG_FILE"])
    OPERATOR_ID = client.operatorAccountId
    with open(os.environ["HEDERA_CONFIG_FILE"]) as f:
        OPERATOR_KEY = PrivateKey.fromString(json.load(f)["operator"]["privateKey"])

else:
    if "OPERATOR_ID" not in os.environ or "OPERATOR_KEY" not in os.environ:
        exit("Must set OPERATOR_ID OPERATOR_KEY environment variables")
    OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
    OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
    HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
    if HEDERA_NETWORK == "previewnet":
        client = Client.forPreviewnet()
    elif HEDERA_NETWORK == "testnet":
        client = Client.forTestnet()
    else:
        client = Client.forMainnet()
    client.setOperator(OPERATOR_ID, OPERATOR_KEY)
