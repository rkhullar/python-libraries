package util

import (
	"encoding/json"
	"fmt"
)

func MapToJSON(data StringMap) string {
	// TODO: move to ordered map?
	result, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	return string(result)
}

func ParseJSON(json_data string) StringMap {
	// TODO: move to ordered map?
	var data StringMap
	err := json.Unmarshal(StrEnc(json_data), &data)
	if err != nil {
		panic(err)
	}
	return data
}

/* TODO
 * adopt bytes.Buffer; buffer.WriteString and buffer.Truncate methods
 * handle nested data
 */
func MarshalOrdered(data StringMap) (ByteSlice, error) {
	result := "{"
	count := 0
	var template string
	for key, value := range data {
		switch value.(type) {
		case string:
			template = `"%s":"%s"`
		default:
			template = `"%s":%v`
		}
		result += fmt.Sprintf(template, key, value) + ","
		count += 1
	}
	if count > 0 {
		result = result[:len(result)-1]
	}
	result += "}"
	return ByteSlice(result), nil
}

/*
 * NOTE: ordered map package
 * - https://pkg.go.dev/github.com/wk8/go-ordered-map/v2
 * - https://github.com/wk8/go-ordered-map
 */
