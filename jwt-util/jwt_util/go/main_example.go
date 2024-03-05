package main

import (
	"fmt"
	core "github.com/rkhullar/python-libraries/jwt-util/core"
)

func main() {
	jwk := core.NewJWK(256, nil)
	fmt.Println(jwk)
	fmt.Println("========")
	key := core.ParseJWK(jwk)
	exported := core.KeyToJSON(key, nil)
	fmt.Println(exported)
	fmt.Println("========")
	fmt.Println("========")
	fmt.Println(jwk == exported)

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
