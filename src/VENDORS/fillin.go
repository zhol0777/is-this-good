// Generates markdown table for use with VENDORS.md

// Usage:
//// <vendor names> <vendor links> <output>
// eg:
//// go run fillin.go vendornames.txt vendorlinks.txt output.txt


package main

import (
	"os"
	"strings"
)
func main(){
	args := os.Args
	names, _ := os.ReadFile(args[1])
	links, _ := os.ReadFile(args[2])
	output := args[3]
	names_list := strings.Split(string(names), "\n")
	links_list := strings.Split(string(links), "\n")
	final_list := make([]string, len(names_list), len(names_list))
	for i := 0; i < len(final_list)-1; i++ {
		final_list[i] = "|[" + names_list[i] + "](" + links_list[i] + ")|||"
	}

	data := strings.Join(final_list, "\n")

	os.WriteFile(string(output), []byte(data), 0777)
}

