package core

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"errors"
	"fmt"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
	"math/big"
)

func NewKey(size int) (*rsa.PrivateKey, error) {
	return rsa.GenerateKey(rand.Reader, size)
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

func ParseMap(data util.StringMap) (*rsa.PrivateKey, error) {
	fields := []string{"n", "e", "d", "p", "q", "dp", "dq", "qi"}
	values, err := util.B64DecBigIntMap(data, fields)
	if err != nil {
		return nil, err
	}
	return &rsa.PrivateKey{
		PublicKey: rsa.PublicKey{
			N: values["n"],
			E: int(values["e"].Int64()),
		},
		D: values["d"],
		Primes: []*big.Int{
			values["p"],
			values["q"],
		},
		Precomputed: rsa.PrecomputedValues{
			Dp:   values["dp"],
			Dq:   values["dq"],
			Qinv: values["qi"],
		},
	}, nil
}

func ParseJWK(jwk string) (*rsa.PrivateKey, error) {
	data, err := util.ParseJSON(jwk)
	if err != nil {
		return nil, err
	}
	return ParseMap(data)
}

func KeyToPEM(key *rsa.PrivateKey) (string, error) {
	bytes, err := x509.MarshalPKCS8PrivateKey(key)
	if err != nil {
		return "", err
	}
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "PRIVATE KEY",
		Bytes: bytes,
	})
	return string(data), nil
}

func ParsePEM(data string) (*rsa.PrivateKey, error) {
	block, _ := pem.Decode(util.StrEnc(data))
	if block == nil {
		return nil, errors.New("failed to decode PEM data")
	}
	var key any
	var err error
	switch block.Type {
	case "RSA PRIVATE KEY":
		key, err = x509.ParsePKCS1PrivateKey(block.Bytes)
	case "PRIVATE KEY":
		key, err = x509.ParsePKCS8PrivateKey(block.Bytes)
	default:
		return nil, fmt.Errorf("unsupported PEM type: %s", block.Type)
	}
	if err != nil {
		return nil, err
	}
	rsaKey, ok := key.(*rsa.PrivateKey)
	if !ok {
		return nil, errors.New("parsed key is not an RSA private key")
	}
	return rsaKey, nil
}
