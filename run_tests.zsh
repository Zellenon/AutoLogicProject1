#!/bin/zsh

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

directory="$1"

if [[ ! -d "$directory" ]]; then
    echo "Error: '$directory' is not a valid directory."
    exit 1
fi

for subdirectory in "$directory"/*; do
    for file in "$subdirectory"/*; do
        if [[ -f "$file" ]]; then
            echo "Testing $file"
            timeout 10 python3 main.py $file
        fi
    done
done