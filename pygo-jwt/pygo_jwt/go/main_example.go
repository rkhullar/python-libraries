package main

import (
	"fmt"
	lib "github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/core"
	"os"
	"os/user"
)

func main() {
	/*
		jwk := lib.NewJWK(1024, nil)
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

		lib.ExampleGo(4)
	*/

	///*

	//headers := lib.StringMap{
	//	"alg": "RS256",
	//	"kid": "asdf",
	//	"typ": "JWT",
	//}
	//payload := lib.StringMap{
	//	"message": "hello world",
	//	"count":   4,
	//	//"nested": map[string]any{
	//	//	"x": 1,
	//	//	"y": false,
	//	//	"z": "asdf",
	//	//},
	//}
	//
	//fmt.Println(headers)
	//fmt.Println(payload)

	me, _ := user.Current()

	jwk_path := "Lab/personal/python-libraries/pygo-jwt/local/data/private-key.json"
	jwk_data, err := os.ReadFile(me.HomeDir + "/" + jwk_path)
	if err != nil {
		panic(err)
	}
	jwk := string(jwk_data)
	//fmt.Println(jwk)

	lib.ParseJWK(jwk)

	//expected := "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFzZGYiLCJ0eXAiOiJKV1QifQ.eyJtZXNzYWdlIjoiaGVsbG8gd29ybGQiLCJjb3VudCI6NH0.y-MJyFJF2fjiTVl-ZlfM64-unANVhKq06tABXu0ju-bilTAtVQ3_pHfinKitla4OMkfy7y1MV-Kt3_6twERyFKbNmTH4kIiIoZbsjDy5D9F8Bri0eqcRDSKGbhmqQp-ohc9fyaF106gZYF0-cETLOg0SBR0QgBeX3Q710t2CLaU"
	//fmt.Println(expected)

	//headers_json := lib.MapToJSON(headers)
	//payload_json := lib.MapToJSON(payload)
	//
	//fmt.Println(headers_json)
	//fmt.Println(payload_json)
	//
	//payload_b64 := lib.B64EncStr(payload_json)
	//fmt.Println(payload_b64)
	//*/

	header_data := "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFzZGYiLCJ0eXAiOiJKV1QifQ"
	payload_data := "eyJtZXNzYWdlIjoiaGVsbG8gd29ybGQiLCJjb3VudCI6NH0"
	expected := "y-MJyFJF2fjiTVl-ZlfM64-unANVhKq06tABXu0ju-bilTAtVQ3_pHfinKitla4OMkfy7y1MV-Kt3_6twERyFKbNmTH4kIiIoZbsjDy5D9F8Bri0eqcRDSKGbhmqQp-ohc9fyaF106gZYF0-cETLOg0SBR0QgBeX3Q710t2CLaU"
	actual := lib.ParseJWKAndSign(jwk, header_data+"."+payload_data)
	fmt.Println(actual)
	fmt.Println(actual == expected)

	public_jwk := lib.ExtractPublicJWK(jwk)
	fmt.Println(public_jwk)
	t := lib.ParsePublicJWKAndVerify(public_jwk, header_data+"."+payload_data, actual)
	fmt.Println(t)

	//fmt.Println(jwk)
	//public_jwk := lib.ExtractPublicJWK(jwk)
	//fmt.Println(public_jwk)

	//public_key := lib.ParsePublicJWK(public_jwk)
	//public_jwk2 := lib.PublicKeyToJSON(public_key, nil)
	//fmt.Println(public_jwk == public_jwk2)

	//pem := lib.JWKToPEM(jwk)
	//fmt.Println(pem)
	//public_pem := lib.ExtractPublicPEM(pem)
	//fmt.Println(public_pem)
	//
	//public_key := lib.ParsePublicPEM(public_pem)
	//public_pem2 := lib.PublicKeyToPEM(public_key)
	//fmt.Println(public_pem == public_pem2)
}
