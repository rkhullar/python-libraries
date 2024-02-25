#!/usr/bin/env sh

set -x
here=$(dirname "$PWD"/"$0")
here=$(cd "$here" || exit; pwd)

rm -rf "$here/local"; mkdir "$here/local"
docker_context="$here/local/docker-context.tar"
tar --exclude='local' --exclude='venv' --exclude='docker' -hcvf "$docker_context" ./*
