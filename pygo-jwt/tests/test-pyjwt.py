# pip install pyjwt cryptography

import jwt
from util import example_payload, read_data

private_pem = read_data('private-key.pem')
token = jwt.encode(payload=example_payload, key=private_pem, algorithm='RS256', headers={'kid': 'asdf'})
print(token)

public_pem = read_data('public-key.pem')
data = jwt.decode(jwt=token, key=public_pem, algorithms=['RS256'])
print(data)
