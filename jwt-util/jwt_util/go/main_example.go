package main

import (
	"fmt"
	"github.com/rkhullar/python-libraries/jwt-util/x"
)

func main() {
	jwk := x.NewJWK(256, nil)
	fmt.Println(jwk)

	//test_json := `{
	//	"d": "5NYey8IunZM9But2h4F8-APSKCD3GWHLwA3KN2J5wgE",
	//	"dp": "2mmTOiZU23ZPOV3qT2F2gQ",
	//	"dq": "QGVmzbwykw6JYfxW3vollQ",
	//	"e": "AQAB",
	//	"kty": "RSA",
	//	"n": "6BOZnFET2J07-kwhQbSbTd3Dcp3xJgNAcVw7cL_dnE0",
	//	"p": "_CRROPYHmhnuqhCFZQTjQQ",
	//	"q": "66Cu_WYR6aIaGzWum0OSDQ",
	//	"qi": "mCsQYWR9Z3OdUNCS0DIdmQ"
	//}`
	//
	//parse_key(test_json)
}
