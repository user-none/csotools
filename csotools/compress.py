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

import os
import struct
import zlib

from .header import CSOHeader

def compress(fin, fout, level=9):
    # Ensure level is within range
    if level > 9:
        level = 9
    if level < 1:
        level = 1

    # Get the uncompressed size
    fin.seek(0, os.SEEK_END)
    uncompressed_size = fin.tell()
    fin.seek(0)

    # Create our header
    header = CSOHeader()
    header.update(1, uncompressed_size)

    # Write the header
    fout.write(header.to_bytes())

    # Write blank data that will be the index table. Which we'll go back
    # and fill in later once we've created it.
    indexes_start = fout.tell()
    num_indexes = (header.uncompressed_size() // header.block_size()) + 1
    fout.write(b''.zfill(num_indexes * 4))
    indexes = []

    # Write data blocks
    while True:
        indexes.append(fout.tell())

        data = fin.read(header.block_size())
        if not data:
            break

        cdata = zlib.compress(data, level=level, wbits=-15)
        if len(cdata) < header.block_size():
            fout.write(cdata)
        else:
            # Mark the index as uncompressed. Bit 32 is set to 1.
            indexes[-1] = indexes[-1] | (1 << 31)
            fout.write(data)

    # Write our real index table
    fout.seek(indexes_start)
    for index in indexes:
        fout.write(struct.pack('<I', index))
