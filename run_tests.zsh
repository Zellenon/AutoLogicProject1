#!/bin/zsh

# Check if a directory argument is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

directory="$1"

# Check if the provided argument is a valid directory
if [[ ! -d "$directory" ]]; then
    echo "Error: '$directory' is not a valid directory."
    exit 1
fi

# Loop through each file in the directory
for subdirectory in "$directory"/*; do
    
    # Loop through each file in the directory
    for file in "$subdirectory"/*; do
        # Check if the current item is a file
        if [[ -f "$file" ]]; then
            # Call your terminal command on each filename here
            # For demonstration, let's echo the filename
            echo "Processing file: $file"
            # Example of running a terminal command on the filename:
            # YourCommandHere "$file"
            timeout 10 python3 main.py $file
        fi
    done
done