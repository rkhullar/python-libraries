import pygo_jwt
from util import read_data, example_payload

private_jwk = read_data('private-key.json')
token = pygo_jwt.encode(payload=example_payload, key=private_jwk, mode='jwk', headers={'kid': 'asdf'})
print(token)
