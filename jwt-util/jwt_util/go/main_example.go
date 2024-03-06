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

	test3 := lib.PEMToJWK(exported2)
	fmt.Println(test3)
	fmt.Println("========")

	fmt.Println(test3 == jwk)
	fmt.Println("========")

}
