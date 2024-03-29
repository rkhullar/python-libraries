#!/usr/bin/env sh

set -x
here=$(dirname "$PWD"/"$0")
here=$(cd "$here" || exit; pwd)
target_path=$(cd "${here}/../.." || exit; pwd)

rm -rf "$here/local"; mkdir "$here/local"
docker_context="$here/local/docker-context.tar"

cd "$target_path" || exit
make clean
tar --exclude='local' --exclude='venv' --exclude='docker' -hcvf "$docker_context" ./*

cd "$here" || exit
tar --append --file "$docker_context" Dockerfile
tar --append --file "$docker_context" --dereference docker-compose.yaml
tar -tvf "$docker_context"

platform=$(yq '.services.builder.platform' docker-compose.yaml)
docker build --platform "$platform" -t pygo-hello-build - < "$docker_context"
rm -rf "$here/local" "$here/out"
docker compose up

## first attempt
# tar --exclude='local' --exclude='venv' -cvh ./* | docker build -t pygo-hello-build -
