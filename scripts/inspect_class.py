#!/usr/bin/env python
"""
usage:
    inspect_class.py followed by class name, for examples:
    for hedera: inspect_class.py Transaction
    for other:  inspect_class.py java.util.List
"""

import os
import sys
import shutil

if len(sys.argv) < 2:
    exit("need a class name")

if "." in sys.argv[1]:
    classname = sys.argv[1]
else:
    classname = "com.hedera.hashgraph.sdk." + sys.argv[1]

if not shutil.which("javap"):
    exit("This script relies on `javap` but it's not found")

base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
java_sdk_dir = os.path.join(base_dir, "hedera-sdk-java")

if not os.path.isdir(java_sdk_dir):
    exit("hedera-sdk-java does not exist")

jar_dir = os.path.join(java_sdk_dir, "sdk", "build", "libs")

jarfiles = os.listdir(jar_dir)
if len(jarfiles) == 0:
    exit("no jar exist, build the jar first")

jar_name = next(reversed(sorted(jarfiles)))
jar_file = os.path.join(jar_dir, jar_name)

os.system("javap -classpath {} -public -s {}".format(jar_file, classname))
