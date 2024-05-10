#!/bin/zsh

directory="./project1-tests"

for file in "$directory"/**/**; do
    echo "-----------------------------"
    echo "Timing $file"
    time python3 main.py $file > /dev/null
done
