#!/usr/bin/env sh

set -x
here=$(dirname "$(realpath "$0")")
target_path="${here}/../"
cd "${target_path}" || exit

rm -rf venv
python -m venv venv
. venv/bin/activate
pip install -U pip setuptools
pip install pipenv
pipenv install --dev
