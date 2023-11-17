import argparse
import subprocess
from shutil import which
from pathlib import Path
from urllib import parse

# Get path of this file
SELF_PATH = Path(__file__).parent.resolve()

parser = argparse.ArgumentParser(description="Build the Docker Image needed")

parser.add_argument(
    "--dockerfile",
    help="Path to the Dockerfile to use",
    default=SELF_PATH / "Dockerfile.in"
)

parser.add_argument(
    "--platform",
    help="Build the image for the given platform",
    default="linux/arm64/v8"
)

parser.add_argument(
    "--tag",
    help="Tag the image with the given tag",
    default="local/arm64"
)

# Number of parallel builds
parser.add_argument(
    "--parallel",
    type=int,
    default=16,
    help="Number of parallel builds"
)

args = parser.parse_args()

def ensure_program_exists(program):
    if which(program) is None:
        raise Exception(f"{program} not found")

# Create the image
ensure_program_exists("docker")

# Open Dockerfile and format {parallel}
with open(SELF_PATH / args.dockerfile, "r") as f:
    dockerfile = f.read()

# dockerfile = dockerfile.format(parallel=args.parallel)

# Write Dockerfile
with open(SELF_PATH / "Dockerfile", "w") as f:
    f.write(dockerfile)

build_cache_dir = SELF_PATH / ".build_cache"
build_cache_dir.mkdir(exist_ok=True)

# Install the qemu packages
subprocess.run([
    "apt-get",
    "install",
    "qemu",
    "binfmt-support",
    "qemu-user-static",
    "-y"
], cwd=SELF_PATH, check=True)

# This step will execute the registering scripts
subprocess.run([
    "docker",
    "run",
    "--rm",
    "--privileged",
    "multiarch/qemu-user-static",
    "--reset",
    "-p",
    "yes"
], cwd=SELF_PATH, check=True)

subprocess.run([
    "docker",
    "buildx",
    "create",
    "--use"
], cwd=SELF_PATH, check=True)

subprocess.run([
    "docker",
    "buildx",
    "build",
    "--cache-from",
    f"type=local,src={build_cache_dir.as_posix()}",
    "--cache-to",
    f"type=local,dest={build_cache_dir.as_posix()}",
    "--platform",
    args.platform,
    "--load",
    "-t",
    args.tag,
    "."
], cwd=SELF_PATH, check=True)

#Prune docker images
subprocess.run([
    "docker",
    "image",
    "prune",
    "-f"
], cwd=SELF_PATH, check=True)
