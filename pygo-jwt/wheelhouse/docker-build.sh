#!/usr/bin/env sh

# check if both parameters are provided
if [ $# -ne 3 ]; then
    echo "usage: $0 <base> <version> <arch>"
    exit 1
fi

# assign parameters to variables
base="$1"
version="$2"
arch="$3"

# check if base is either "alpine" or "sam"
if [ "$base" != "alpine" ] && [ "$base" != "aws-sam" ]; then
    echo "error: base must be either 'alpine' or 'aws-sam'"
    exit 1
fi

# check if arch is either "amd64" or "arm64"
if [ "$arch" != "amd64" ] && [ "$arch" != "arm64" ]; then
    echo "error: arch must be either 'amd64' or 'arm64'"
    exit 1
fi

# infer base image
if [ "$base" == "alpine" ]; then
    base_image="python:${version}-alpine"
elif [ "$base" == "aws-sam" ]; then
    base_image="public.ecr.aws/sam/build-python${version}"
fi

command="docker build --build-arg BASE_IMAGE=${base_image} --platform linux/${arch} -t test-${base}-${arch} ."
echo "$command"
eval "$command"

# ./docker-build.sh aws-sam 3.12 amd64
# ./docker-build.sh alpine 3.12 amd64
# ./docker-build.sh aws-sam 3.12 arm64
# ./docker-build.sh alpine 3.12 arm64

# docker run -it --rm --platform linux/amd64 test-aws-sam-amd64
# docker run -it --rm --platform linux/amd64 test-alpine-amd64
# docker run -it --rm --platform linux/arm64 test-aws-sam-arm64
# docker run -it --rm --platform linux/arm64 test-alpine-arm64
