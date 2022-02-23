#!/bin/bash

# Utility script to help with marking as a TA. Takes the most recent file in 
# the user's Downloads folder and renames it using the given argument name. Also
# prefixes the name with a number starting from 0

if [ $# -eq 0 ]; then
    echo "Error: No name given"
    exit 0
fi

# Get current file number.
max=-1
files="*.c"
regex="^([0-9]+)_.*\.c$"
for f in $files; do
    if [[ $f =~ $regex ]]; then
        num=${BASH_REMATCH[1]}
        if [ $num -gt $max ]; then
            max=$num
        fi
    fi
done

((max += 1))

# Get the most recent element
newestDownload=$(ls -Art ~/Downloads | tail -n 1)
mv ~/Downloads/$newestDownload ./$max"_"$1.c