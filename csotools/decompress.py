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

import struct
import zlib

from .header import CSOHeader
from .block_index import CSOBlockIndex

def decompress(fin, fout):
    fin.seek(0)
    header = CSOHeader()
    header.parse(fin.read(24))

    if header.version() != 0 and header.version() != 1:
        raise Exception('Unsupported CSO version')

    indexes = []
    for i in range((header.uncompressed_size() // header.block_size()) + 1):
        index = struct.unpack('<I', fin.read(4))[0]
        indexes.append(index)
    indexes = [ CSOBlockIndex(indexes[i], indexes[i+1], header.index_alignment()) for i in range(len(indexes)-1) ]

    for index in indexes:
        fin.seek(index.start())
        if index.compressed():
            data = zlib.decompress(fin.read(index.idx_len()), wbits=-15, bufsize=header.block_size() * 2)
        else:
            data = fin.read(index.idx_len())

        fout.write(data)
