'''
from jwt_util import ExtensionAdapter

adapter = ExtensionAdapter()
jwk = adapter.new_jwk()
print(jwk)
pem = adapter.jwk_to_pem(jwk)
print(pem)

adapter.example_go(4)
'''

# '''
from pathlib import Path

import jwt

import pygo_jwt
from pygo_jwt import ExtensionAdapter


def read_data(name: str) -> str:
    path = Path(__file__).parent / 'data' / name
    with path.open('r') as f:
        return f.read().strip()


test_jwk = read_data('private-key.json')
test_pem = read_data('private-key.pem')

payload = {'message': 'hello world', 'count': 4, "nested": {"x": 1, "a": 2}}
result_a = jwt.encode(payload=payload, key=test_pem, algorithm='RS256', headers={'kid': 'asdf'})
print(result_a)

print()

result_b = pygo_jwt.encode(payload=payload, key=test_jwk, mode='jwk', headers={'kid': 'asdf'})
print(result_b)

print(result_a == result_b)

public_jwk = ExtensionAdapter.extract_public_jwk(test_jwk)
public_pem = ExtensionAdapter.extract_public_pem(test_pem)

print(public_jwk)
print(public_pem)

token_parts = result_b.split('.')
assert len(token_parts) == 3
print(token_parts)
x = ExtensionAdapter.parse_public_jwk_and_verify(key=public_jwk, data=f'{token_parts[0]}.{token_parts[1]}', signature=token_parts[2])
print(x)
y = ExtensionAdapter.parse_public_pem_and_verify(key=public_pem, data=f'{token_parts[0]}.{token_parts[1]}', signature=token_parts[2])
print(y)
# '''