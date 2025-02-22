# hedera-sdk-py examples

As hedera-sdk-py use Java SDK underneath, you must have Java Runtime or JDK installed.

Copy `.env.sample` to `.env` and enter your own java location, id and private key.

If you use a network other than testnet, set `HEDERA_NETWORK` environment variable to either 'mainnet' or 'previewnet'.  

Alternatively you can use a config json file.  2 examples are provided: client-config.json and client-config-with-operator.json.  See `client_from_file.py` for an example of using config file instead of using environment variables.

A few examples can be used in groups. For example:

File related:

    python create_file.py
    # a node_id and a file_id will be printed
    python get_file_contents.py id_from_above
    python file_append_chunked.py file_id  # takes 2 minutes
    python get_file_contents.py file_id  # content changed
    python delete_file.py file_id

To subscribe to HCS topics, use `PyConsumer` functional interface. However, it's recommended to use a seperate program.  Please see [hcs-grpc-client](https://github.com/wensheng/hcs-grpc-api-py-client) for using Python gRPC client to subscribe to HCS topic on Hedera mirror nodes without using SDK.
