#!/bin/zsh

directory="./project1-tests"

for subdirectory in "$directory"/*; do
    for file in "$subdirectory"/*; do
        if [[ -f "$file" ]]; then
            echo "Testing $file"
            timeout 10 python3 main.py $file
        fi
    done
done