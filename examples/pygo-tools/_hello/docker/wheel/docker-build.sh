#!/usr/bin/env sh

set -x
here=$(dirname "$(realpath "$0")")
target_path="${here}/../"
cd "${target_path}" || exit

make clean
# tar --exclude='local' --exclude='venv' -cvh ./* | docker build -t pygo-hello-build -
tar --exclude='local' --exclude='venv' -cvf docker-context.tar ./*
# docker compose up
