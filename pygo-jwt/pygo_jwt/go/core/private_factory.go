package core

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
	"math/big"
)

func NewKey(size int) *rsa.PrivateKey {
	key, err := rsa.GenerateKey(rand.Reader, size)
	if err != nil {
		panic(err)
	}
	return key
}

func KeyToMap(key *rsa.PrivateKey, id *string) util.StringMap {
	E := big.NewInt(int64(key.E))
	data := util.StringMap{
		"kty": "RSA",
		"n":   util.B64Enc(key.N.Bytes()),
		"e":   util.B64Enc(E.Bytes()),
		"d":   util.B64Enc(key.D.Bytes()),
		"p":   util.B64Enc(key.Primes[0].Bytes()),
		"q":   util.B64Enc(key.Primes[1].Bytes()),
		"dp":  util.B64Enc(key.Precomputed.Dp.Bytes()),
		"dq":  util.B64Enc(key.Precomputed.Dq.Bytes()),
		"qi":  util.B64Enc(key.Precomputed.Qinv.Bytes()),
	}
	if id != nil {
		data["kid"] = *id
	}
	return data
}

func ParseMap(data util.StringMap) *rsa.PrivateKey {
	return &rsa.PrivateKey{
		PublicKey: rsa.PublicKey{
			N: util.B64DecBigInt(data["n"]),
			E: int(util.B64DecBigInt(data["e"]).Int64()),
		},
		D: util.B64DecBigInt(data["d"]),
		Primes: []*big.Int{
			util.B64DecBigInt(data["p"]),
			util.B64DecBigInt(data["q"]),
		},
		Precomputed: rsa.PrecomputedValues{
			Dp:   util.B64DecBigInt(data["dp"]),
			Dq:   util.B64DecBigInt(data["dq"]),
			Qinv: util.B64DecBigInt(data["qi"]),
		},
	}
}

func ParseJWK(jwk string) *rsa.PrivateKey {
	data := util.ParseJSON(jwk)
	return ParseMap(data)
}

func KeyToPEM(key *rsa.PrivateKey) string {
	bytes, err := x509.MarshalPKCS8PrivateKey(key)
	if err != nil {
		panic(err)
	}
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "PRIVATE KEY",
		Bytes: bytes,
	})
	return string(data)
}

func ParsePEM(data string) *rsa.PrivateKey {
	block, _ := pem.Decode(util.StrEnc(data))
	if block == nil {
		panic("failed to decode PEM data")
	}
	var key any
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
