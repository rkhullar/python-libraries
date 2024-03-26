package core

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"errors"
	"fmt"
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

func PublicKeyToJSON(key *rsa.PublicKey, id *string) (string, error) {
	data := PublicKeyToMap(key, id)
	return util.MapToJSON(data)
}

func PublicKeyToPEM(key *rsa.PublicKey) (string, error) {
	bytes, err := x509.MarshalPKIXPublicKey(key)
	if err != nil {
		return "", err
	}
	data := pem.EncodeToMemory(&pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: bytes,
	})
	return string(data), nil
}

func ExtractPublicJWK(jwk string) (string, error) {
	data, err := util.ParseJSON(jwk)
	if err != nil {
		return "", err
	}
	key, err := ParseMap(data)
	if err != nil {
		return "", err
	}
	kid := util.StringMap_GetStrPtr(data, "kid")
	return PublicKeyToJSON(&key.PublicKey, kid)
}

func ExtractPublicPEM(pem string) (string, error) {
	key, err := ParsePEM(pem)
	if err != nil {
		return "", err
	}
	return PublicKeyToPEM(&key.PublicKey)
}

func ParsePublicMap(data util.StringMap) (*rsa.PublicKey, error) {
	fields := []string{"n", "e"}
	values, err := util.B64DecBigIntMap(data, fields)
	if err != nil {
		return nil, err
	}
	return &rsa.PublicKey{
		N: values["n"],
		E: int(values["e"].Int64()),
	}, nil
}

func ParsePublicJWK(jwk string) (*rsa.PublicKey, error) {
	data, err := util.ParseJSON(jwk)
	if err != nil {
		return nil, err
	}
	return ParsePublicMap(data)
}

func ParsePublicPEM(data string) (*rsa.PublicKey, error) {
	block, _ := pem.Decode(util.StrEnc(data))
	if block == nil {
		return nil, errors.New("failed to decode PEM data")
	}
	var key any
	var err error
	switch block.Type {
	case "RSA PUBLIC KEY":
		key, err = x509.ParsePKCS1PublicKey(block.Bytes)
	case "PUBLIC KEY":
		key, err = x509.ParsePKIXPublicKey(block.Bytes)
	default:
		return nil, fmt.Errorf("unsupported PEM type: %s", block.Type)
	}
	if err != nil {
		return nil, err
	}
	rsaKey, ok := key.(*rsa.PublicKey)
	if !ok {
		return nil, errors.New("parsed key is not an RSA public key")
	}
	return rsaKey, nil
}
