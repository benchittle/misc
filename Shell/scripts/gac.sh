#!/bin/bash

# git add . && git commit -m "$1"
# Commits current folder using first argument as commit message.

if [ $# -eq 0 ]; then
    echo "ERROR: You must supply a commit message"
    return 1
fi
git add .
if [ $? -eq 0 ]; then
    git commit -m "$1"
fi
