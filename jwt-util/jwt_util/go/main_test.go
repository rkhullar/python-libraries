package main

import "testing"
import "gotest.tools/assert"

func TestBuildSignature(t *testing.T) {
	t.Run("canary", func(t *testing.T) {
		assert.Equal(t, "hello world", build_signature())
	})
}
