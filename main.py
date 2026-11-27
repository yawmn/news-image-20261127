#!/usr/bin/env python3
"""news-image-20261127 -- THE GLOBAL DISPATCH entry program.

Writes the pre-rendered 1024x1024 broadsheet (entry.png, bundled beside
this file) to the output directory as entry.png, then validates the
bytes it wrote: PNG signature, per-chunk CRCs, IHDR dimensions within
the kit cap (1024x1024), total size within 1 MiB, and an IEND
terminator. Deterministic: the same input bytes always produce the
same output bytes. No network, no clock, no randomness, and no
temporary files inside the output directory -- the file is written
directly to its final name and chmodded 0644.

Usage:
    python3 main.py [--check | --self-test | --version]
The output directory is $MAKEFUN_OUTPUT_DIR, else /output.
"""

import hashlib
import os
import struct
import sys
import zlib

VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_source():
    """Read the bundled broadsheet bytes."""
    with open(SOURCE, "rb") as fh:
        return fh.read()


def validate_png(data):
    """Check the PNG is whole and within the kit limits.

    Returns (width, height). Raises ValueError on any defect.
    """
    if len(data) > MAX_BYTES:
        raise ValueError("entry exceeds the 1 MiB cap: %d bytes" % len(data))
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG (bad signature)")
    pos = 8
    width = height = None
    seen_iend = False
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            raise ValueError("truncated chunk %r" % ctype)
        chunk = data[pos + 4:end - 4]
        (stored_crc,) = struct.unpack(">I", data[end - 4:end])
        if zlib.crc32(chunk) & 0xFFFFFFFF != stored_crc:
            raise ValueError("bad CRC in chunk %r" % ctype)
        if ctype == b"IHDR":
            if length != 13:
                raise ValueError("bad IHDR length")
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
            if width > MAX_DIM or height > MAX_DIM:
                raise ValueError("dimensions %dx%d exceed 1024x1024"
                                 % (width, height))
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                raise ValueError("trailing bytes after IEND")
            break
        pos = end
    if width is None:
        raise ValueError("no IHDR chunk")
    if not seen_iend:
        raise ValueError("no IEND chunk")
    return width, height


def run(outdir):
    """Write entry.png into outdir and validate what was written."""
    data = read_source()
    width, height = validate_png(data)
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, "entry.png")
    # Direct write to the final name: no temp file is ever created
    # inside the output directory (the kit rejects those at grading).
    with open(dest, "wb") as fh:
        fh.write(data)
    os.chmod(dest, 0o644)
    written = open(dest, "rb").read()
    if written != data:
        raise ValueError("written bytes differ from source")
    validate_png(written)
    digest = hashlib.sha256(written).hexdigest()
    print("wrote %s: %dx%d, %d bytes, sha256 %s"
          % (dest, width, height, len(written), digest))
    return dest


def self_test():
    """Run the entry twice into throwaway dirs and compare bytes."""
    import tempfile
    first = None
    for i in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            dest = run(tmp)
            blob = open(dest, "rb").read()
            if first is None:
                first = blob
            elif blob != first:
                raise ValueError("non-deterministic output on run %d" % (i + 1))
            mode = oct(os.stat(dest).st_mode & 0o777)
            if mode != "0o644":
                raise ValueError("entry.png mode is %s, expected 0o644" % mode)
    print("self-test ok: two runs byte-identical, mode 0644")


def main(argv):
    if "--version" in argv:
        print("news-image-20261127 main.py %s" % VERSION)
        return 0
    if "--self-test" in argv:
        self_test()
        return 0
    if "--check" in argv:
        data = read_source()
        width, height = validate_png(data)
        print("check ok: %dx%d, %d bytes, sha256 %s"
              % (width, height, len(data),
                 hashlib.sha256(data).hexdigest()))
        return 0
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    run(outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
