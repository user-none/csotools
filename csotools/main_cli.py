#!/usr/bin/env python

# Copyright 2022 John Schember <john@nachtimwald.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import sys

import csotools

def parse_args():
    parser = argparse.ArgumentParser(
            prog = os.path.basename(sys.argv[0]),
            description = 'Compress ISO and decompress CSO files')
    parser.add_argument('in_file', help='Input file name. Can be CSO (decompress) or ISO (compress)')
    parser.add_argument('out_file', help='Output file name')
    parser.add_argument('-l ', '--level', type=int, default=9, help='CSO v1 compression level. Only when compressing 1 - 9')
    parser.add_argument('--version', action='version', version='%(prog)s {v}'.format(v=csotools.__version__))
    parser.add_argument('-s', '--stats', action='store_true', help='print statistic informatation')
    return parser.parse_args()

def compress_cso(fin, fout, level, stats=False):
    csotools.compress(fin, fout, level)

    if stats:
        fin.seek(0, os.SEEK_END)
        fout.seek(0, os.SEEK_END)
        print('compressed: {p}% smaller'.format(p=int(fout.tell()/fin.tell()*100)))

def decompress_cso(fin, fout, stats=False):
    csotools.decompress(fin, fout)

    if stats:
        fin.seek(0, os.SEEK_END)
        fout.seek(0, os.SEEK_END)
        print('decompressed: {p}% larger'.format(p=int(fout.tell()/fin.tell()*100)))

def main():
    args = parse_args()

    try:
        with open(args.in_file, 'rb') as fin, open(args.out_file, 'w+b') as fout:
            if csotools.is_cso(fin.read(4)):
                decompress_cso(fin, fout, args.stats)
            else:
                compress_cso(fin, fout, args.level, args.stats)
    except Exception as e:
        print(e)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
