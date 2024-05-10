#!/bin/zsh

directory="./project1-tests"

for file in "$directory"/**/**; do
    echo "-----------------------------"
    echo "Timing $file"
    time python3 main.py $file > /dev/null
done

# for subdirectory in "$directory"/*; do
#     for file in "$subdirectory"/*; do
#         if [[ -f "$file" ]]; then
#             echo "Testing $file iteration 1"
#             timeout 10 python3 main.py $file
#             echo "Testing $file iteration 2"
#             timeout 10 python3 main.py $file
#         fi
#     done
# done
