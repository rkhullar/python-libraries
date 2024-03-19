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
import jwt_util


def read_data(name: str) -> str:
    path = Path(__file__).parent / 'data' / name
    with path.open('r') as f:
        return f.read().strip()


test_jwk = read_data('private-key.json')
test_pem = read_data('private-key.pem')

payload = {'message': 'hello world', 'count': 4}
result = jwt.encode(payload=payload, key=test_pem, algorithm='RS256', headers={'kid': 'asdf'})
print(result)

print()

x = jwt_util.encode(payload=payload, key=test_pem, headers={'kid': 'asdf'})
print(x)
# '''