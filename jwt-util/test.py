from jwt_util import ExtensionAdapter

adapter = ExtensionAdapter()
jwk = adapter.new_jwk()
print(jwk)
pem = adapter.jwk_to_pem(jwk)
print(pem)
