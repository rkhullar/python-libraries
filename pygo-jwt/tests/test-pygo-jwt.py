from util import example_payload, read_data

import pygo_jwt

private_jwk = read_data('private-key.json')
token = pygo_jwt.encode(payload=example_payload, key=private_jwk, mode='jwk', headers={'kid': 'asdf'})
print(token)

public_jwk = read_data('public-key.json')
data = pygo_jwt.decode(token=token, key=public_jwk, mode='jwk')
print(data)
