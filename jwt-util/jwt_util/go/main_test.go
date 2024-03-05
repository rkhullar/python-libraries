package main

import (
	core "github.com/rkhullar/python-libraries/jwt-util/core"
	"testing"
)
import "gotest.tools/assert"

func TestBuildSignature(t *testing.T) {
	t.Run("canary", func(t *testing.T) {
		assert.Equal(t, "hello world", core.BuildSignature())
	})
}
