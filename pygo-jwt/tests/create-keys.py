from util import write_data

import pygo_jwt

private_jwk = pygo_jwt.new_jwk(size=512, _id='asdf')
private_pem = pygo_jwt.jwk_to_pem(private_jwk)

print(private_jwk)
print(private_pem)

public_jwk = pygo_jwt.extract_public_jwk(private_jwk)
public_pem = pygo_jwt.extract_public_pem(private_pem)

print(public_jwk)
print(public_pem)

write_data(name='private-key.json', data=private_jwk)
write_data(name='private-key.pem', data=private_pem)
write_data(name='public-key.json', data=public_jwk)
write_data(name='public-key.pem', data=public_pem)
