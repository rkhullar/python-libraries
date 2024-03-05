package x

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"math/big"
)

func NewKey(size int) *rsa.PrivateKey {
	key, err := rsa.GenerateKey(rand.Reader, size)
	if err != nil {
		panic(err)
	}
	return key
}

func KeyToJSON(key *rsa.PrivateKey, id *string) string {
	data := KeyToMap(key, id)
	return MapToJSON(data)
}

func KeyToMap(key *rsa.PrivateKey, id *string) StringMap {
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

func NewJWK(size int, id *string) string {
	key := NewKey(size)
	return KeyToJSON(key, id)
}

func ParseJWK(json_data string) *rsa.PrivateKey {
	data := ParseJSON(json_data)
	n := b64dec(data["n"])
	e := b64dec(data["e"])
	d := b64dec(data["d"])
	p := b64dec(data["p"])
	q := b64dec(data["q"])
	dp := b64dec(data["dp"])
	dq := b64dec(data["dq"])
	qi := b64dec(data["qi"])
	return &rsa.PrivateKey{
		PublicKey: rsa.PublicKey{
			N: new(big.Int).SetBytes(n),
			E: int(new(big.Int).SetBytes(e).Int64()),
		},
		D: new(big.Int).SetBytes(d),
		Primes: []*big.Int{
			new(big.Int).SetBytes(p),
			new(big.Int).SetBytes(q),
		},
		Precomputed: rsa.PrecomputedValues{
			Dp:   new(big.Int).SetBytes(dp),
			Dq:   new(big.Int).SetBytes(dq),
			Qinv: new(big.Int).SetBytes(qi),
		},
	}
}

func KeyToPEM(key *rsa.PrivateKey) string {
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(key),
	})
	return string(data)
}

func JWKToPem(json_data string) string {
	key := ParseJWK(json_data)
	return KeyToPEM(key)
}

func BuildSignature() string {
	return "hello world"
}
