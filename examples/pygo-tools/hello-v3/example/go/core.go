package main

import "fmt"

func hello(message string, count int) string {
	return fmt.Sprintf("hello %s %d", message, count)
}
