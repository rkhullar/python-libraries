## pygo-jwt

### Example Go Usage

```shell
go mod init main
go get github.com/rkhullar/python-libraries/jwt-util/jwt_util/go
```

```go
package main

import (
	"fmt"
	lib "github.com/rkhullar/python-libraries/jwt-util/jwt_util/go/core"
)

func main() {
	key := lib.NewJWK(2048, nil)
	fmt.Println(key)
}
```
