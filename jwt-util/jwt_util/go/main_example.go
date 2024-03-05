package main

import (
	"fmt"
	lib "github.com/rkhullar/python-libraries/jwt-util/core"
)

func main() {
	jwk := lib.NewJWK(256, nil)
	fmt.Println(jwk)
	fmt.Println("========")

	key := lib.ParseJWK(jwk)
	exported := lib.KeyToJSON(key, nil)

	fmt.Println(exported)
	fmt.Println("========")

	fmt.Println(jwk == exported)
	fmt.Println("========")

	exported2 := lib.KeyToPEM(key)
	fmt.Println(exported2)
	fmt.Println("========")

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
