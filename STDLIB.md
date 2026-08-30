# Standard Library Usage

Zero-dep is designed to run without third-party Python dependencies.

## Standard Library Modules Used

| Module | Purpose |
|---|---|
| argparse | Command-line interface |
| collections.OrderedDict | LRU cache implementation |
| dataclasses | Structured result objects |
| hashlib | SHA-256 checksums |
| json | Search-index persistence |
| math | TF-IDF calculations |
| os | File-system operations |
| pathlib | File and path handling |
| re | Text tokenization |
| struct | Binary storage record encoding and decoding |

## Third-Party Alternatives

The project avoids third-party packages where they would normally be used.

| Normally used | Standard-library alternative |
|---|---|
| requests / urllib3 | pathlib / os for local file operations |
| database libraries | struct + binary files |
| checksum libraries | hashlib |
| regex/tokenization packages | re |
| cache libraries | collections.OrderedDict |
| serialization libraries | json |
| numerical libraries | math |
| CLI frameworks | argparse |
| data-model libraries | dataclasses |

## Zero-Dependency Policy

The application source code does not import third-party Python packages.

The files `requirements.txt` and `.zero-dep.toml` are intentionally empty.

`pytest` is used only for automated testing and is not a runtime dependency.
