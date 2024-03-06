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
