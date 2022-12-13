#!/bin/bash

mkdir .opt

#convert jpg to png
for image in *.jpg; do
    convert  "$image"  "${image%.jpg}.png"
done

#reduce size
for ext in "jpg" "png"; do
    for image in *.$ext; do
        jpegoptim –size=200k -d .opt -p "$image"
    done
done


