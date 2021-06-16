# hedera-sdk-py examples

As hedera-sdk-py use Java SDK underneath, you need to set your JAVA_HOME to jre/jdk >=11.

Linux example: **`export JAVA_HOME=/usr/lib/jvm/jdk-11.0.11`**

For Windows, use **'Advanced System Settings', 'Environment Variables...'**.

For most examples, you need to set `OPERATOR_ID` and `OPERATOR_KEY` environment variables.

On Linux:

    export OPERATOR_ID=your_id
    export OPERATOR_KEY=your_private_key
    
On Windows:

    set OPERATOR_ID=your_id
    set OPERATOR_KEY=your_private_key

They are used in get_client.py, which was imported into most examples.  If you use network other than testnet, set `HEDERA_NETWORK` environment variable.  

Alternatively you can use a config json file.  2 examples are provided: client-config.json and client-config-with-operator.json.  See `client_from_file.py` for an example of using config file instead of using environment variables.

A few examples can be used in groups. For example:

File related:

    python create_file.py
    # a node_id and a file_id will be printed
    python get_file_contents.py id_from_above
    python file_append_chunked.py node_id file_id  # takes 2 minutes
    python get_file_contents.py file_id  # content changed
    python delete_file.py file_id
    
