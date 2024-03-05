package main

import (
	"github.com/rkhullar/python-libraries/jwt-util/x"
	"testing"
)
import "gotest.tools/assert"

func TestBuildSignature(t *testing.T) {
	t.Run("canary", func(t *testing.T) {
		assert.Equal(t, "hello world", x.BuildSignature())
	})
}
