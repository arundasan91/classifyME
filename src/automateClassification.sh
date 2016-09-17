#!/usr/bin/env bash

dir=/home/cc/imagesFromRpi/
app=/home/cc/classifyME/src/caffeClassification.py

inotifywait -m "$dir" --format '%w%f' -e close_write |
    while read file; do
         python "$app" "$file"
    done
