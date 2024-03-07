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

func ParseJWK(jwk string) *rsa.PrivateKey {
	data := ParseJSON(jwk)
	return ParseMap(data)
}

func ParseMap(data StringMap) *rsa.PrivateKey {
	return &rsa.PrivateKey{
		PublicKey: rsa.PublicKey{
			N: b64dec_bigint(data["n"]),
			E: int(b64dec_bigint(data["e"]).Int64()),
		},
		D: b64dec_bigint(data["d"]),
		Primes: []*big.Int{
			b64dec_bigint(data["p"]),
			b64dec_bigint(data["q"]),
		},
		Precomputed: rsa.PrecomputedValues{
			Dp:   b64dec_bigint(data["dp"]),
			Dq:   b64dec_bigint(data["dq"]),
			Qinv: b64dec_bigint(data["qi"]),
		},
	}
}

func KeyToPEM(key *rsa.PrivateKey) string {
	// TODO: consider PKCS8 format?
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(key),
	})
	return string(data)
}

func JWKToPEM(jwk string) string {
	key := ParseJWK(jwk)
	return KeyToPEM(key)
}

func PEMToJWK(data string) string {
	key := ParsePEM(data)
	return KeyToJSON(key, nil)
}

func ParsePEM(data string) *rsa.PrivateKey {
	block, _ := pem.Decode(strenc(data))
	if block == nil {
		panic("failed to decode PEM data")
	}
	var key interface{}
	var err error
	switch block.Type {
	case "RSA PRIVATE KEY":
		key, err = x509.ParsePKCS1PrivateKey(block.Bytes)
	case "PRIVATE KEY":
		key, err = x509.ParsePKCS8PrivateKey(block.Bytes)
	default:
		panic("unsupported PEM type")
	}
	if err != nil {
		panic(err)
	}
	rsaKey, ok := key.(*rsa.PrivateKey)
	if !ok {
		panic("parsed key is not an RSA private key")
	}
	return rsaKey
}

func BuildSignature() string {
	return "hello world"
}
