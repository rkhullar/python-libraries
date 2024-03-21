package core

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/util"
	"math/big"
)

func PublicKeyToMap(key *rsa.PublicKey, id *string) util.StringMap {
	E := big.NewInt(int64(key.E))
	data := util.StringMap{
		"kty": "RSA",
		"e":   util.B64Enc(E.Bytes()),
		"n":   util.B64Enc(key.N.Bytes()),
		"alg": "RS256",
		"use": "sig",
	}
	if id != nil {
		data["kid"] = *id
	}
	return data
}

func PublicKeyToJSON(key *rsa.PublicKey, id *string) string {
	data := PublicKeyToMap(key, id)
	return util.MapToJSON(data)
}

func PublicKeyToPEM(key *rsa.PublicKey) string {
	bytes, err := x509.MarshalPKIXPublicKey(key)
	if err != nil {
		panic(err)
	}
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: bytes,
	})
	return string(data)
}

func ExtractPublicJWK(jwk string) string {
	data := util.ParseJSON(jwk)
	key := ParseMap(data)
	kid := util.StringMap_GetStrPtr(data, "kid")
	return PublicKeyToJSON(&key.PublicKey, kid)
}

func ExtractPublicPEM(pem string) string {
	key := ParsePEM(pem)
	return PublicKeyToPEM(&key.PublicKey)
}

func ParsePublicMap(data util.StringMap) *rsa.PublicKey {
	return &rsa.PublicKey{
		N: util.B64DecBigInt(data["n"]),
		E: int(util.B64DecBigInt(data["e"]).Int64()),
	}
}

func ParsePublicJWK(jwk string) *rsa.PublicKey {
	data := util.ParseJSON(jwk)
	return ParsePublicMap(data)
}

func ParsePublicPEM(data string) *rsa.PublicKey {
	block, _ := pem.Decode(util.StrEnc(data))
	if block == nil {
		panic("failed to decode PEM data")
	}
	var key any
	var err error
	switch block.Type {
	case "RSA PUBLIC KEY":
		key, err = x509.ParsePKCS1PublicKey(block.Bytes)
	case "PUBLIC KEY":
		key, err = x509.ParsePKIXPublicKey(block.Bytes)
	default:
		panic("unsupported PEM type")
	}
	if err != nil {
		panic(err)
	}
	rsaKey, ok := key.(*rsa.PublicKey)
	if !ok {
		panic("parsed key is not an RSA public key")
	}
	return rsaKey
}
