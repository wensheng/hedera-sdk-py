# hedera-sdk-py
[Hedera](https://hedera.com/) SDK in Python

This is basically a python wrapper of [Hedera SDK in Java](https://github.com/hashgraph/hedera-sdk-java).

## Install

    pip install hedera-sdk-py


## How to Use
```python
from hedera import PrivateKey
prikey = PrivateKey.generate()
print("Private key: {}".format(prikey.toString()))
print("Public key: {}".format(prikey.getPublicKey().toString()))
```
You must make sure JAVA_HOME is set to a JRE/JDK that's >=11. Do a `echo $JAVA_HOME` on Linux/MacOS or `echo %JAVA_HOME%` on Windows to confirm.

MacOS example:

    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-16.0.2.jdk/Contents/Home

Linux example:

    export JAVA_HOME=/usr/lib/jvm/java-16-openjdk-amd64

Windows:

Type to search "advanced system", you should see "View Advanced System settings", click it, then click "Environment Variables..."

On Windows, if you get "no jvm dll found" error, you need to add %JAVA_HOME%/bin/server (i.e. C:\Program Files\Java\jdk-11.0.10\bin\server) to your path.

See [examples](https://github.com/wensheng/hedera-sdk-py/tree/main/examples) for more example usages.

