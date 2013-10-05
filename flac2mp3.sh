#!/bin/sh
set -eux

# don't split args on whitespace (enables support for filenames containing spaces)
SAVEIFS=$IFS
IFS=$(echo "\n\b")

# config
TO_EXT=.mp3
FROM_EXT=.flac

# parse args
target_dir=$1

# transcode files
for file in $(find "$target_dir" -name "*$FROM_EXT"); do
    flac --decode --stdout "$file" | lame --preset extreme - "$target_dir/`basename $file $FROM_EXT`$TO_EXT"
done

# restore env settings
IFS=$SAVEIFS

