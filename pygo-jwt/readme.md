## pygo-jwt

This project focusing on managing json web tokens signed with RS256. Inspired from [`pyjwt`](https://pypi.org/project/PyJWT)
this library provides the core`encode` and `decode` functionality, but uses the standard `crypto` package within Go instead
of [`cryptography`](https://pypi.org/project/cryptography).

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
	key := lib.NewJWK(2048, nil)
	fmt.Println(key)
}
```
