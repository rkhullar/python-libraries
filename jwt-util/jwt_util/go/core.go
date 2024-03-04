package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/json"
	"fmt"
	"math/big"
)

func build_key(size int, id *string) string {
	private_key, err := rsa.GenerateKey(rand.Reader, size)
	if err != nil {
		panic(err)
	}
	E := big.NewInt(int64(private_key.E))
	private_jwk := map[string]interface{}{
		"kty": "RSA",
		"n":   b64enc(private_key.N.Bytes()),
		"e":   b64enc(E.Bytes()),
		"d":   b64enc(private_key.D.Bytes()),
		"p":   b64enc(private_key.Primes[0].Bytes()),
		"q":   b64enc(private_key.Primes[1].Bytes()),
		"dp":  b64enc(private_key.Precomputed.Dp.Bytes()),
		"dq":  b64enc(private_key.Precomputed.Dq.Bytes()),
		"qi":  b64enc(private_key.Precomputed.Qinv.Bytes()),
	}
	if id != nil {
		private_jwk["kid"] = *id
	}
	private_jwk_json, err := json.Marshal(private_jwk)
	if err != nil {
		panic(err)
	}
	return string(private_jwk_json)
}

func parse_key(json_data string) {
	var data map[string]interface{}
	err := json.Unmarshal([]byte(json_data), &data)
	if err != nil {
		panic(err)
	}
	d := new(big.Int)
	d.SetString(data["d"].(string), 10)
	result := &rsa.PrivateKey{
		PublicKey:   rsa.PublicKey{},
		D:           d,
		Primes:      nil,
		Precomputed: rsa.PrecomputedValues{},
	}
	fmt.Println(result)
}

func jwk_to_pem() {
}

func build_signature() string {
	return "hello world"
}
