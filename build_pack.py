#!/usr/bin/env python3
"""Build only the reviewed, pinned 25-key Transmog Japanese resource pack."""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANG = 'assets/transmog/lang/ja_jp.json'
LICENSE_SHA256 = 'a366506974a46752dbf54c187288b5d5de7f4570422b0cbacd4f5cd1dcb8f099'
EXPECTED_KEYS = {
    'block.transmog.transmogrification_table', 'item.transmog.void_fragment',
    'tag.item.transmog.transmog_fuels',
    'transmog.config.disable_during_pvp_duration',
    'transmog.config.disable_during_pvp_duration.label',
    'transmog.config.disable_during_pvp_duration.tooltip',
    'transmog.config.render', 'transmog.config.render.everywhere',
    'transmog.config.render.everywhere.tooltip', 'transmog.config.render.in_world',
    'transmog.config.render.in_world.tooltip', 'transmog.config.render.off',
    'transmog.config.render.off.tooltip', 'transmog.config.tooltip',
    'transmog.config.tooltip.full', 'transmog.config.tooltip.full.tooltip',
    'transmog.config.tooltip.minimal', 'transmog.config.tooltip.minimal.tooltip',
    'transmog.config.tooltip.none', 'transmog.config.tooltip.none.tooltip',
    'transmog.config_title', 'transmog.creative_tab', 'transmog.transmog_container',
    'transmog.transmog_description', 'transmog.transmog_hidden',
}
EXPECTED_PACK = {
    'pack': {'description': 'ATM11 日本語改善: Transmog（25項目）',
             'min_format': [84, 0], 'max_format': [84, 0]},
    'filter': {'block': [{'namespace': '^transmog$', 'path': r'^lang/ja_jp\.json$'}]},
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_file(root, name):
    path = root / name
    for part in (path, *path.parents):
        if part == root:
            break
        require(not part.is_symlink(), f'Symlink is not allowed: {name}')
    return path.read_bytes()


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs)


def package_bytes(root):
    release_raw = read_file(root, 'release.json')
    release = parse(release_raw)
    require(set(release) == {'schema_version', 'version', 'review_status', 'language_sha256'} and release['schema_version'] == 1,
            'Unexpected release.json schema')
    require(release['review_status'] == 'accepted', 'Independent language review is pending; no ZIP generated')
    require(isinstance(release['version'], str) and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?', release['version']), 'Invalid release version')
    require(isinstance(release['language_sha256'], str) and re.fullmatch('[0-9a-f]{64}', release['language_sha256']), 'Missing reviewed language SHA-256')
    pack_raw = read_file(root, 'resourcepack/pack.mcmeta')
    require(parse(pack_raw) == EXPECTED_PACK, 'Only pack format 84.0 and the exact Transmog language filter are permitted')
    language_raw = read_file(root, 'resourcepack/' + LANG)
    require(digest(language_raw) == release['language_sha256'], 'Language bytes changed after review; SHA-256 mismatch')
    language = parse(language_raw)
    require(isinstance(language, dict) and set(language) == EXPECTED_KEYS, 'All and only the 25 Transmog keys are required')
    require(all(isinstance(value, str) and value.strip() for value in language.values()), 'Every translation must be a nonempty string')
    pack_files = set()
    for path in (root / 'resourcepack').rglob('*'):
        require(not path.is_symlink(), 'Resource pack contains a symlink')
        if path.is_file():
            pack_files.add(str(path.relative_to(root / 'resourcepack')))
    require(pack_files == {'pack.mcmeta', LANG}, 'Unexpected file in resourcepack; refusing to include it')
    license_raw = read_file(root, 'LICENSES/Transmog-MIT.txt')
    require(digest(license_raw) == LICENSE_SHA256, 'Upstream MIT license bytes changed')
    files = {'pack.mcmeta': pack_raw, LANG: language_raw,
             'LICENSES/Transmog-MIT.txt': license_raw, 'release.json': release_raw,
             'README.md': read_file(root, 'README.md'), 'NOTICE.md': read_file(root, 'NOTICE.md')}
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    return release['version'], output.getvalue()


def main():
    try:
        version, raw = package_bytes(ROOT)
        directory = ROOT / 'dist'
        require(not directory.is_symlink(), 'dist must not be a symlink')
        directory.mkdir(exist_ok=True)
        output = directory / f'ATM11-Japanese-Transmog-{version}.zip'
        if output.exists() or output.is_symlink():
            require(not output.is_symlink() and output.is_file() and output.read_bytes() == raw,
                    'Existing release ZIP has different bytes; use a new version instead of overwriting it')
        else:
            fd, name = tempfile.mkstemp(prefix='.pack-', dir=directory)
            temporary = Path(name)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                # Install without clobbering a file created by another process.
                os.link(temporary, output)
            finally:
                temporary.unlink()
        print(f'PACK OK: dist/{output.name}')
        print(f'SHA-256: {digest(raw)}')
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'BUILD REFUSED: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
