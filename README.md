# CSO compression and decompression tool

CSO is a compressed ISO9660 format that is commonly used by PlayStation
Portable (PSP) UMD disk images.

This tool provides:

1. Command line tool for compressing and decompressing CSO files
2. Python module with compression and decompression routines

# CLI

When using the CLI interface autodetection of the input file takes
place to determine if compression or decompression should take place.
if the input file is a CSO file it will be decompressed. If it is not
a CSO file it will be compressed as CSO. No validation of the input
file format (whether it is ISO9660) takes place.

The CLI interface can be run from the top level project
source directory. E.g.:

## Running

Running from the package directory:

```
python -m csotools.main_cli file.iso out.cso
```

If installed on the system using a system package manager or `pip`:

```
csotools file.iso out.cso
```

# Module

Three functions are exposed by the `csotools` module:

## Functions

### `csotools.compress(in_file, out_file)`
 
`in_file` will be compressed as CSO and the compressed data will be saved to `out_file`.

In file and out file are file type objects. Due to the size of ISO9660 files it is
recommended to use file objects and not in memory file like objects.

### `csotools.decompress(in_file, out_file)`
 
`in_file` will be decompressed from CSO and the uncompressed data will be saved to `out_file`.
If `in_file` is not a CSO file an exception will be thrown.

In file and out file are file type objects. Due to the size of ISO9660 files it is
recommended to use file objects and not in memory file like objects.

### `csotools.is_cso(data)`

Checks whether the given data is a CSO file. This only checks the first 4 bytes are the
CSO file marker. `data` should be at least 4 bytes.

## Example

```
from csotools import is_cso
print(is_cso(b'1234'))
```
