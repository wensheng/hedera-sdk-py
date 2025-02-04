#!/usr/bin/env python

import os
import sys
import shutil
from zipfile import ZipFile
# from subprocess import Popen, PIPE
# from tqdm import tqdm

# no longer need to javap since we bring all abstract classes and interfaces out
#   as they have public static methods
# if not shutil.which("javap"):
#     exit("This script relies on `javap` but it's not found")

base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
java_sdk_dir = os.path.join(base_dir, "hiero-sdk-java")

if not os.path.isdir(java_sdk_dir):
    exit("hiero-sdk-java does not exist, did you forget to checkout submodule?")

jar_dir = os.path.join(java_sdk_dir, "sdk", "build", "libs")


# TODO: build jar

jarfiles =  os.listdir(jar_dir)
if len(jarfiles) == 0:
    exit("no jar exist, build the jar first")

jar_name = next(reversed(sorted(jarfiles)))
version = jar_name[4:-4]
jar_file = os.path.join(jar_dir, jar_name)
new_jar_file = os.path.join(base_dir, "src", "hedera", jar_name)
shutil.copy2(jar_file, new_jar_file)

fw = open(os.path.join(base_dir, "src", "hedera", "generated.py"), 'w')
fw.write(f"""import os
from dataclasses import dataclass
here = os.path.abspath(os.path.dirname(__file__))
os.environ['CLASSPATH'] = os.path.join(here, "{jar_name}")
from jnius import autoclass, PythonJavaClass, java_method

__version__ = "{version}"
JString = autoclass("java.lang.String")
JStandardCharsets = autoclass("java.nio.charset.StandardCharsets")
JInstant = autoclass("java.time.Instant")
JDuration = autoclass("java.time.Duration")

""")

names_to_export = ["__version__", "JString", "JStandardCharsets", "JInstant", "JDuration", "PyConsumer", "MirrorResponse"]

with ZipFile(jar_file) as zf:
    namelist = [a for a in zf.namelist() if 
                a.startswith("com/hedera/hashgraph/sdk/") and 
                a.endswith(".class") and 
                not "-" in a and
                not "hashgraph/sdk/proto" in a]

    # for i in tqdm(namelist):
    for i in namelist:
        java_classname = i[:-6].replace("/",".")
        # with Popen(["javap", "-classpath", jar_file, "-public", classname], stdout=PIPE) as proc:
        #    output = proc.stdout.readlines()
        #    if 'abstract class' not in output[1].decode() and not '$' in classname:
        #        fw.write("{} = autoclass('{}')\n".format(classname[25:], classname))
        if not '$' in java_classname:
            autoclass_name = java_classname[java_classname.rindex(".") + 1:]
            fw.write("{} = autoclass('{}')\n".format(autoclass_name, java_classname))
            names_to_export.append(autoclass_name)

fw.write("""

@dataclass(frozen=True)
class MirrorResponse:
    timestamp: str
    sequence_number: float
    contents: str

class PyConsumer(PythonJavaClass):
    __javainterfaces__ = ['java/util/function/Consumer']

    def __init__(self, fn):
        self.fn = fn

    @java_method('(Ljava/lang/Object;)V')
    def accept(self, msg) -> MirrorResponse:
        timestamp = msg.consensusTimestamp.toString()
        sequence_number = msg.sequenceNumber
        contents = JString(msg.contents, JStandardCharsets.UTF_8).toString()
        self.fn(MirrorResponse(timestamp, sequence_number, contents))


""")

formatted_exports = ',\n'.join(f'\t"{classname}"' for classname in names_to_export)
fw.write("__all__ = [\n{}\n]".format(formatted_exports))

fw.close()
