#!/usr/bin/env python3
"""Ship the Monday 23 November 2026 news poster.

The picture itself is entry.png in this folder, painted earlier by
draw_poster.py. This program checks the picture is a genuine 1024 by
1024 PNG under the 1 MiB limit, then hands an identical copy to the
output folder the grader reads (first command-line argument, else
MAKEFUN_OUTPUT_DIR, else ./out).

Pure standard library, no network, no randomness: the same input
always produces the same output bytes.
"""

import hashlib
import os
import struct
import sys

POSTER = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
SIZE_LIMIT = 1024 * 1024
BLOCK = 65536

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def poster_dimensions(path):
    """Read width and height out of the PNG header, or raise."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: bad signature")
    if head[12:16] != b"IHDR":
        raise ValueError("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def destination_folder(argv):
    if len(argv) > 1 and argv[1]:
        return argv[1]
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "out")


def ship():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, POSTER)
    width, height = poster_dimensions(source)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "poster is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    source_size = os.path.getsize(source)
    if source_size > SIZE_LIMIT:
        raise ValueError("poster is %d bytes, over the 1 MiB limit" % source_size)

    out_dir = destination_folder(sys.argv)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, POSTER)

    source_hash = hashlib.sha256()
    dest_hash = hashlib.sha256()
    with open(source, "rb") as reader:
        with open(dest, "wb") as writer:
            while True:
                block = reader.read(BLOCK)
                if not block:
                    break
                source_hash.update(block)
                writer.write(block)
    os.chmod(dest, 0o644)
    with open(dest, "rb") as handle:
        while True:
            block = handle.read(BLOCK)
            if not block:
                break
            dest_hash.update(block)
    if source_hash.hexdigest() != dest_hash.hexdigest():
        raise ValueError("copy digest mismatch: output is not identical")
    print(
        "entry.png %dx%d (%d bytes) -> %s sha256 %s"
        % (width, height, source_size, dest, dest_hash.hexdigest())
    )
    return 0


def main():
    try:
        return ship()
    except (OSError, ValueError) as problem:
        print("main.py: %s" % problem, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
