# CSO format

CSO is a compressed ISO9660 format that is commonly used by PlayStation
Portable (PSP) UMD disk images.

There are two versions of the CSO format, v1 and v2. v1 uses deflate
compression and v2 uses both deflate and LZ4.

# Structure

The CSO is structured into three parts.

1. Header
2. Index table
3. Data

The uncompressed data is sliced into individual blocks using a block size defined in the header.

## Header

The header is fixed length and is 24 bytes.

Offsets and lengths are in bytes. Little endian architecture is used.
Which is the same as the PSP

Name              | Offset | Size | Description
----------------- | ------ | ---- | -----------
Magic             | 0      | 4    | Identifies the file is a CSO file. [ 'C', 'I', 'S', 'O' ] or 0x4F534943
Header Size       | 4      | 4    | Should always be 24
Uncompressed Size | 8      | 8    | Size of uncompressed ISO data
Block Size        | 16     | 4    | Size of each uncompressed data block. Typically 2048 the same as ISO9660 sectors
Version           | 20     | 1    | CSO version. v1 can be 0 or 1. v2 must be 2
Index Alignment   | 21     | 1    | Bit alignment of each index in the index table 
Reserved          | 22     | 2    | Data reserved space. Should be 00 for v2 format

## Index table

The index table is an array of 1 byte block information. The byte is broken down in bits 1-31 and bit 32.

Name     | Bit | Length | Description
-------- | --- | ------ | -----------
Position | 0   | 31     | The position within the CSO file that the block begins
Compress | 32  | 1      | Whether the block is compressed and what compression method is used

The `position` should be masked with `0x7FFFFFFF` to remove the compression bit.
After masking the position is shifted left by the alignment defined in the header.
A block size could be larger than the data within the block due to alignment being used.
Hence needing to use the `next - current` position to get the block size then the aliment
shift to get the data size.

The `compression` can be determined by masking with `0x80000000` and shifting right `>> 31`.
When creating a block index and marked it as compressed would be `|= (1 << 31)`.

The length of a block is found by subtracting the position from the position in the next index within
the index table. Due to this there will always be 1 more index that represents the end of the last block.

### Compression

Each block is compressed independently of other blocks.

- v1 uses `0` for deflate and `1` for uncompressed data.
- v2 used `0` for deflate and `1` for LZ4.

## Data

Compressed or uncompressed data.

If a compressed block would end up the same or larger than the block size defined in the header the data
is left uncompressed. As such you can have a mix of compressed and uncompressed blocks within the CSO file.
Compressed blocks and the last block (possibility) will be smaller than the block size.
