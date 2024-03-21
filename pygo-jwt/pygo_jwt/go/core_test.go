package main

import (
	"fmt"
	lib "github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/core"
	"testing"
)
import "gotest.tools/assert"

func TestFactory(t *testing.T) {
	t.Run("general", func(t *testing.T) {
		key_id := "asdf"
		private_jwk := lib.NewJWK(16, &key_id)
		private_pem := lib.JWKToPEM(private_jwk)
		private_jwk2 := lib.PEMToJWK(private_pem, &key_id)
		fmt.Println(private_jwk)
		fmt.Println(private_pem)
		assert.Equal(t, private_jwk, private_jwk2)
		public_jwk := lib.ExtractPublicJWK(private_jwk)
		public_pem := lib.ExtractPublicPEM(private_pem)
		fmt.Println(public_jwk)
		fmt.Println(public_pem)
		assert.Equal(t, "hello world", "hello world")
	})
}
