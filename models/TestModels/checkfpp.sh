#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if the base file is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <base_file_name>"
    exit 1
fi

# Assign the base file name
base_file="$1.fpp"
ref_file="$1.ref.fpp"

# Check if both files exist
if [ ! -f "$base_file" ]; then
    echo "Error: Base file '$base_file' not found."
    exit 1
fi

if [ ! -f "$ref_file" ]; then
    echo "Error: Reference file '$ref_file' not found."
    exit 1
fi

# Compare the files
if cmp -s "$base_file" "$ref_file"; then
    echo -e "$1.fpp --> ${GREEN}PASS${NC}"
else
    echo -e "$1.fpp --> ${RED}FAIL${NC}"
    echo "Differences:"
    diff "$base_file" "$ref_file"
fi

