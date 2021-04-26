#!/usr/bin/env python

import os
import sys
import shutil
from subprocess import Popen, PIPE
from zipfile import ZipFile
from tqdm import tqdm

if not shutil.which("javap"):
    exit("This script relies on `javap` but it's not found")

base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
java_sdk_dir = os.path.join(base_dir, "hedera-sdk-java")

if not os.path.isdir(java_sdk_dir):
    exit("hedera-sdk-java does not exist, did you forget to checkout submodule?")

jar_dir = os.path.join(java_sdk_dir, "sdk", "build", "libs")


# TODO: build jar

jarfiles =  os.listdir(jar_dir)
if len(jarfiles) == 0:
    exit("no jar exist, build the jar first")

jar_name = next(reversed(sorted(jarfiles)))
jar_file = os.path.join(jar_dir, jar_name)
new_jar_file = os.path.join(base_dir, "src", "hedera", jar_name)
shutil.copy2(jar_file, new_jar_file)

fw = open(os.path.join(base_dir, "src", "hedera", "generated.py"), 'w')
fw.write("""import os
here = os.path.abspath(os.path.dirname(__file__))
os.environ['CLASSPATH'] = os.path.join(here, "%s")
from jnius import autoclass


""" % jar_name)

with ZipFile(jar_file) as zf:
    namelist = [a for a in zf.namelist() if 
                a.startswith("com/hedera/hashgraph/sdk/") and 
                a.endswith(".class") and 
                not "-" in a and
                not "hashgraph/sdk/proto" in a]

    for i in tqdm(namelist):
        classname = i[:-6].replace("/",".")
        # print("javap -classpath {} -public {}".format(jar_file, classname))
        with Popen(["javap", "-classpath", jar_file, "-public", classname], stdout=PIPE) as proc:
            output = proc.stdout.readlines()
            if 'abstract class' not in output[1].decode() and not '$' in classname:
                fw.write("{} = autoclass('{}')\n".format(classname[25:], classname))

fw.close()
#print(jarfile)
#print(base_dir)
#java_sdk_dir
#
#if [ ! -f ${JAR} ]; then
#    echo "No such file: ${JAR}"
#    exit
#fi

