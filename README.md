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

see [examples](https://github.com/wensheng/hedera-sdk-py/tree/main/examples) for more example usages.

## How to Build
(**Ignore this section unless you want to contribute or make custom SDK**)

Hedera-sdk-py requires JDK >=11, either OpenJDK or Oracle JDK.

Clone this repo:

    git clone --recurse-submodules https://github.com/wensheng/hedera-sdk-py.git

Patch Java code:

    patch -p 1 -d hedera-sdk-java < patches/961b6dc9.patch

To insure patching success, check out the commit whose hash match the patch filename.  For example:

    cd hedera-sdk-java
    git checkout 961b6dc9
    cd ..
    patch -p 1 -d hedera-sdk-java < patches/961b6dc9.patch

As of now (2021/4), the difference is very minimal, no java source code is changed, only build.gradle's are modified to ensure jar packaging. But in the future, java source code might be modified to provide convience for interacting with SDK in Python.

You can revert the patches:

    cd hedera-sdk-java
    git reset --hard

Build the Jar (make sure JAVA_HOME set to a JDK that's >=11):

    cd hedera-sdk-java
    ./gradlew uberJar

Generate code (make sure tqdm is installed):

    python scripts/generate_code.py

Build package:

    rm -fr build dist
    python -m build

Test package (preferably inside a virtual env or pipenv):

    pip uninstall hedera-sdk-py
    pip install dist/hedera_sdk_py-(current_version)-py3-none-any.whl

Upload to Pypi (don't do this unless you're me):

    python -m twine upload dist/*
