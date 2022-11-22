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

CSO_MAGIC = 0x4F534943 # 'CISO'

class CSOHeader():
    # Header layout with default values
    _magic = CSO_MAGIC
    _header_size = 24
    _uncompressed_size = 0
    _block_size = 2048
    _version = 1
    _index_alignment = 0
    _reserved = [ 0, 0 ]

    def parse(self, data: bytes):
        '''
        Parse a 24 byte binary header into the header object
        '''

        if len(data) < 24:
            raise Exception('Not enough header data')

        magic = struct.unpack('<I', data[0:4])[0]
        if magic != CSO_MAGIC:
            raise Exception('Not a CSO header')

        self._magic = magic
        self._header_size = struct.unpack('<i', data[4:8])[0]
        self._uncompressed_size = struct.unpack('<Q', data[8:16])[0]
        self._block_size = struct.unpack('<I', data[16:20])[0]
        self._version = struct.unpack('<B', data[20:21])[0]
        self._index_alignment = struct.unpack('<B', data[21:22])[0]
        self._reserved = struct.unpack('<2B', data[22:24])

    def to_bytes(self):
        return struct.pack('<IiQIBB2B',
                           self._magic,
                           self._header_size,
                           self._uncompressed_size,
                           self._block_size,
                           self._version,
                           self._index_alignment,
                           self._reserved[0],
                           self._reserved[1])

    def update(self, version, uncompressed_size):
        self._uncompressed_size = uncompressed_size
        self._version = version

    def __str__(self):
        out = []

        out.append('MAGIC:             {m}'.format(m=[ chr(x) for x in struct.unpack('<4B', struct.pack('<i', self._magic)) ]))
        out.append('HEADER SIZE:       {s}'.format(s=self._header_size))
        out.append('UNCOMPRESSED SIZE: {u}'.format(u=self._uncompressed_size))
        out.append('BLOCK SIZE:        {b}'.format(b=self._block_size))
        out.append('VERSION:           {v}'.format(v=self._version))
        out.append('INDEX ALIGN        {i}'.format(i=self._index_alignment))
        out.append('RESERVED           {r1}{r2}'.format(r1=self._reserved[0], r2=self._reserved[1]))

        return '\n'.join(out)

    def uncompressed_size(self):
        return self._uncompressed_size

    def block_size(self):
        return self._block_size

    def version(self):
        return self._version

    def index_alignment(self):
        return self._index_alignment

def is_cso(data: bytes):
    if len(data) < 4:
        return False

    magic = struct.unpack('<I', data[0:4])[0]
    if magic != CSO_MAGIC:
        return False
    return True
