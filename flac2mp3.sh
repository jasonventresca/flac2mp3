#!/bin/sh
set -eux

SAVEIFS=$IFS
IFS=$(echo "\n\b")

TO_EXT=.mp3
FROM_EXT=.flac
dir='/Volumes/Space/Downloads/drive_ost'

for file in $(find "$dir" -name "*$FROM_EXT"); do
    flac --decode --stdout "$file" | lame --preset extreme - "`basename $file $FROM_EXT`$TO_EXT"
done

IFS=$SAVEIFS

