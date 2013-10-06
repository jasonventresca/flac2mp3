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
    output_filename = '%s.mp3' % filename
    flac = subprocess.Popen(['flac', '--decode', '--stdout', filename], stdout=subprocess.PIPE)
    lame = subprocess.check_output(['lame', '--preset', 'extreme', '-', output_filename], stdin=flac.stdout)
    flac.wait()


def main(source_dir, target_dir):
    pattern = '*%s' % FROM_EXT
    for filename in glob_files(source_dir, pattern):
        print "transcoding", filename
        transcode(filename)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='flac > mp3 transcoding utility')
    parser.add_argument('-s', '--source-dir', help='the top directory to find %s files' % FROM_EXT)
    parser.add_argument('-t', '--target-dir', help='the directory to write transcoded files will be written')
    args = parser.parse_args()

    main(args.source_dir, args.target_dir)

