## Generic FastAPI

This project demonstrates how to use `nydev-fastapi-tools` to create a generic backend for storing data in MongoDB Atlas.
From the OpenAPI docs, users first log in through Auth0. Then, users can manage their own arbitrary data, or they can read
shared data. Admins can manage shared data.

### Local Development
```shell
asdf local python 3.12.1
./scripts/setup-venv.sh
```
```shell
. venv/bin/activate
python server.py
```
