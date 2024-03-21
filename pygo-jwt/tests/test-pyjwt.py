# pip install pyjwt cryptography

import jwt
from util import read_data, example_payload

private_pem = read_data('private-key.pem')
public_pem = read_data('public-key.pem')
token = jwt.encode(payload=example_payload, key=private_pem, algorithm='RS256', headers={'kid': 'asdf'})
print(token)

data = jwt.decode(jwt=token, key=public_pem, algorithms=['RS256'])
print(data)
