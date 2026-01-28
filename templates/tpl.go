package main

import (
	"encoding/base64"
	"fmt"
	"os"
	"strings"
)

func main() {{
    // Slice of base64 chunks
	chunks := []string{{
{chunks}
	}}

    // Join chunks
	b64 := strings.Join(chunks, "")
    
    // Decode base64 string to bytes
	payload, err := base64.StdEncoding.DecodeString(b64)
	if err != nil {{
		fmt.Println("Error decoding base64:", err)
		return
	}}

    // Write bytes to file with 0644 permissions
	err = os.WriteFile("{filename}", payload, 0644)
	if err != nil {{
		fmt.Println("Error writing file:", err)
		return
	}}

	fmt.Printf("Wrote %d bytes to {filename}\\n", len(payload))
}}
