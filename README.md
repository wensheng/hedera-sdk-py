# hedera-sdk-py
Hedera SDK in Python

## How to Build

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

Build the Jar (make sure JAVA_HOME set to a JDK that's >=11):

    cd hedera-sdk-java
    ./gradlew uberJar
