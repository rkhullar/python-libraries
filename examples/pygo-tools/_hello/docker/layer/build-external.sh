#!/usr/bin/env sh

set -x
here=$(dirname "$PWD"/"$0")
here=$(cd "$here" || exit; pwd)

cd "$here" || exit
rm -rf "$here/local"; mkdir "$here/local"
docker_context="$here/local/docker-context.tar"
tar --exclude='local' --exclude='venv' --exclude='docker' -hcvf "$docker_context" ./*
tar -tvf "$docker_context"

docker build -t pygo-hello-build-layer - < "$docker_context"
rm -rf "$here/local" "$here/out"
docker compose up
