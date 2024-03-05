package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/json"
	"fmt"
	"math/big"
)

func new_key(size int) *rsa.PrivateKey {
	key, err := rsa.GenerateKey(rand.Reader, size)
	if err != nil {
		panic(err)
	}
	return key
}

func key_to_json(key *rsa.PrivateKey, id *string) string {
	data := key_to_dict(key, id)
	return to_json(data)
}

func key_to_dict(key *rsa.PrivateKey, id *string) StringMap {
	E := big.NewInt(int64(key.E))
	data := StringMap{
		"kty": "RSA",
		"n":   b64enc(key.N.Bytes()),
		"e":   b64enc(E.Bytes()),
		"d":   b64enc(key.D.Bytes()),
		"p":   b64enc(key.Primes[0].Bytes()),
		"q":   b64enc(key.Primes[1].Bytes()),
		"dp":  b64enc(key.Precomputed.Dp.Bytes()),
		"dq":  b64enc(key.Precomputed.Dq.Bytes()),
		"qi":  b64enc(key.Precomputed.Qinv.Bytes()),
	}
	if id != nil {
		data["kid"] = *id
	}
	return data
}

func new_jwk(size int, id *string) string {
	key := new_key(size)
	return key_to_json(key, id)
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
