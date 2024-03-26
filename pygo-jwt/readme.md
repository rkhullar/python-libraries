## pygo-jwt

This project focuses on managing JSON Web Tokens signed with RS256. Inspired by [pyjwt](https://pypi.org/project/PyJWT),
this library provides core encode and decode functionality, utilizing the standard `crypto` package within Go instead of
[cryptography](https://pypi.org/project/cryptography).

### Example Usage for Python

```shell
pip install pygo-jwt
```

```python
import pygo_jwt

private_jwk = pygo_jwt.new_jwk(size=2048)
private_pem = pygo_jwt.jwk_to_pem(private_jwk)

public_jwk = pygo_jwt.extract_public_jwk(private_jwk)
public_pem = pygo_jwt.extract_public_pem(private_pem)

payload = {'message': 'hello world', 'count': 4}
token = pygo_jwt.encode(payload=payload, key=private_pem, mode='pem')
token_data = pygo_jwt.decode(token=token, key=public_jwk, mode='jwk')
```

### Example Usage for Go

```shell
go mod init main
go get github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go
```

```go
package main

import (
	"fmt"
	lib "github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/core"
)

func main() {
	private_jwk, _ := lib.NewJWK(2048, nil)
	private_pem, _ := lib.JWKToPEM(private_jwk)
	fmt.Println(private_jwk)
	fmt.Println(private_pem)
}
```
