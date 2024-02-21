#!/usr/bin/env sh

set -x
here=$(dirname "$PWD"/"$0")
here=$(cd "$here" || exit; pwd)
target_path=$(cd "${here}/../.." || exit; pwd)

cd "$target_path" || exit
make clean
# tar --exclude='local' --exclude='venv' -cvh ./* | docker build -t pygo-hello-build -
tar --exclude='local' --exclude='venv' -cvf "$here/local/docker-context.tar" ./*
# docker compose up
