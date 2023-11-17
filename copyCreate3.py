# Used to copy needed files from include and lib directories in Docker Image to rpi-sysroot in another Docker image

import os
import shutil
import subprocess
import argparse

# Docker Image IP Args
parser = argparse.ArgumentParser(description="Build the Docker Image needed")

parser.add_argument(
    "--sourceID",
    help="Name of the source Docker Image",
    default="local/arm64"
)

parser.add_argument(
    "--destID",
    help="Name of the destination Docker Image",
    default="qtpi/qtpi:1.0"
)

args = parser.parse_args()

# Copy lib files
subprocess.run([
    "docker",
    "cp",
    f"{args.sourceID}:/create3/build/prefix/lib",
    "."
])

# Copy include files
subprocess.run([
    "docker",
    "cp",
    f"{args.sourceID}:/create3/build/prefix/include",
    "."
])

# Copy files in lib to rpi-sysroot/lib
subprocess.run([
    "docker",
    "cp",
    "lib",
    f"{args.destID}:/home/qtpi/rpi-sysroot/usr/"
])

# Copy files in include to rpi-sysroot/include
subprocess.run([
    "docker",
    "cp",
    "include",
    f"{args.destID}:/home/qtpi/rpi-sysroot/usr/"
])

# Remove lib and include directories
shutil.rmtree("lib")
shutil.rmtree("include")
