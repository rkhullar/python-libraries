# pip install pyjwt cryptography

import jwt
from util import read_data, example_payload

private_pem = read_data('private-key.pem')
token = jwt.encode(payload=example_payload, key=private_pem, algorithm='RS256', headers={'kid': 'asdf'})
print(token)
