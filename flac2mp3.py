#!/usr/bin/python

import fnmatch
import os
import subprocess

# config
TO_EXT = '.mp3'
FROM_EXT = '.flac'


def glob_files(source_dir, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(source_dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))

    return matches


def transcode(filename):
    # strip trailing '.flac' extension from source filename
    filename_no_ext = FROM_EXT.join(filename.split(FROM_EXT)[:-1])
    # replace with '.mp3' extension
    output_filename = '%s%s' % (filename_no_ext, TO_EXT)

    # do the actual transcoding
    print "transcoding %s --> %s" % (filename, output_filename)
    flac = subprocess.Popen(['flac', '--decode', '--stdout', filename], stdout=subprocess.PIPE)
    lame = subprocess.check_output(['lame', '--preset', 'extreme', '-', output_filename], stdin=flac.stdout)
    flac.wait()


def main(source_dir):
    pattern = '*' + FROM_EXT
    for filename in glob_files(source_dir, pattern):
        transcode(filename)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='flac > mp3 transcoding utility')
    parser.add_argument('-s', '--source-dir', help='the top directory to find %s files' % FROM_EXT)
    args = parser.parse_args()

    main(args.source_dir)

