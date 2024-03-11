package util

import (
	"encoding/json"
	"fmt"
)

func MapToJSON(data StringMap) string {
	result, err := MarshalOrdered(data)
	if err != nil {
		panic(err)
	}
	return string(result)
}

func ParseJSON(json_data string) StringMap {
	var data StringMap
	err := json.Unmarshal(strenc(json_data), &data)
	if err != nil {
		panic(err)
	}
	return data
}

func MarshalOrdered(data StringMap) (ByteArray, error) {
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
	return ByteArray(result), nil
}
