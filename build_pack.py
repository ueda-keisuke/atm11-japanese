#!/usr/bin/env python3
"""Build the separate base and Jade Japanese packs from pinned release evidence."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = '0.3.0'
TRANSMOG_FILTER = {'block': [{'namespace': '^transmog$', 'path': r'^lang/ja_jp\.json$'}]}
POLICIES = {
    'transmog': {
        'version': '1.8.0+26.1',
        'jar_sha256': '71236a1adcec1a6186828c49dd22d330054db30f7372b8d8be25a1c58d704ba7',
        'jar_entry': 'assets/transmog/lang/en_us.json',
        'source_sha256': '89ebb4d6af7d4da87fafaa8e69534b29534a68e6af8532f6d5bc2ea88412be5f',
    },
    'jei': {
        'version': '29.36.0.96',
        'jar_sha256': 'a4ac2d91b2f86e56275316ac185208d275edcca6d975998a93cc6e604910c07d',
        'jar_entry': 'assets/jei/lang/en_us.json',
        'source_sha256': 'b39dc5633aeadb953a671ac50e58a26951b20593473995bbf93a389caae108e1',
    },
    'appleskin': {
        'version': '3.0.9',
        'jar_sha256': '32bfe1ed3dea0684259568dbf2b6fe02e939bf398e54af383238bb3b8cac4da6',
        'jar_entry': 'assets/appleskin/lang/en_us.json',
        'source_sha256': 'e4ecdf6e503c5e9a63277b1092c7221671724959907152ac18cef12cc59f7075',
    },
    'controlling': {
        'version': '26.1.2.4',
        'jar_sha256': '16289226a72a8709d77e2f477beaf276d4a90583efc712c6114811fd1a3a3f51',
        'jar_entry': 'assets/controlling/lang/en_us.json',
        'source_sha256': 'ddd09483c4b6c3b898ca28e3b22e8fb4b042abc402bdef50c1a12cb49fe27725',
    },
    'jade': {
        'version': '26.1.10',
        'jar_sha256': 'd1e477ed030f96605a2471c0d2003846a90cc12c4059782e62cdee2d4c529fc7',
        'jar_entry': 'assets/jade/lang/en_us.json',
        'source_sha256': '799373d21b23e9a8fda3158ff4d098e4d1e6cf99eb2b935836650dce4a459153',
    },
}
# Exact current English key sets: SHA-256 of compact UTF-8 JSON of sorted keys.
# These are counts of keys, including search terms and preserved metadata, not screens.
KEY_SETS = {
    'transmog': (25, 'b369562a850d8b4f2fdf4c3065d0582904bc886a63b675b92e4f6f08c81562ff'),
    'jei': (335, 'd937bcace1710a07a4c1a156d35b1f4046f9663ab67f9b8e534ce6c87e5a2907'),
    'appleskin': (22, '69aad68d780252788180e59a29c4e3a4457f47fc29ad3a2cf920ac1fb4ae332c'),
    'controlling': (12, 'bd5a753a17d7eb4acf894cf43b58d4a4c3f7b25a35f18e754d839c18d18207b1'),
    'jade': (496, '2abacb74df2a08a3058933548c1bb1418fe401c8c62f4338a409cedf3852cb44'),
}
PRESERVED_METADATA_KEYS = {
    'transmog': [], 'jei': ['_comment'], 'appleskin': [], 'controlling': [],
    'jade': ['__comment', 'jade.metadata'],
}
LICENSES = {
    'LICENSES/Project-MIT.txt': '14e77f04a42df608a6346aeacb757acf56aaba69450ff1dbf4b1e0fed3bbc08c',
    'LICENSES/Transmog-MIT.txt': 'a366506974a46752dbf54c187288b5d5de7f4570422b0cbacd4f5cd1dcb8f099',
    'LICENSES/JEI-MIT.txt': '108c93a97f3011c196b8226f5019a9c09ade318fe3a802be2f7f5ddb2c3a0d04',
    'LICENSES/AppleSkin-Unlicense.txt': '88d9b4eb60579c191ec391ca04c16130572d7eedc4a86daa58bf28c6e14c9bcd',
    'LICENSES/Controlling-MIT.txt': 'bd03ec3e3879605835ea5239cb6304b0d5694074d924b050c7099acbb89a5813',
    'LICENSES/Jade-CC-BY-NC-SA-4.0.md': '03d7d5b3f4b37a576d52db87542ac248e161fc47412192e9543c6a71a82b0ff3',
}
PACKAGES = {
    'base': {
        'directory': 'resourcepack', 'release': 'release.json', 'notice': 'NOTICE.md',
        'filename': 'ATM11-Japanese-0.3.0.zip',
        'namespaces': ('transmog', 'jei', 'appleskin', 'controlling'),
        'licenses': ('LICENSES/Project-MIT.txt', 'LICENSES/Transmog-MIT.txt', 'LICENSES/JEI-MIT.txt',
                     'LICENSES/AppleSkin-Unlicense.txt', 'LICENSES/Controlling-MIT.txt'),
        'pack': {
            'pack': {'description': 'ATM11 日本語改善: Transmog / JEI / AppleSkin / Controlling',
                     'min_format': [84, 0], 'max_format': [84, 0]},
            'filter': TRANSMOG_FILTER,
        },
    },
    'jade': {
        'directory': 'resourcepack-jade', 'release': 'release-jade.json', 'notice': 'NOTICE-Jade.md',
        'filename': 'ATM11-Japanese-Jade-0.3.0.zip', 'namespaces': ('jade',),
        'licenses': ('LICENSES/Jade-CC-BY-NC-SA-4.0.md',),
        'pack': {'pack': {'description': 'ATM11 日本語改善: Jade (CC BY-NC-SA 4.0)',
                         'min_format': [84, 0], 'max_format': [84, 0]}},
    },
}
JEI_METADATA_VALUE = 'Debug (for a debug mode, do not need translation)'
# The whole original JAR is pinned above. This is the original JA runtime setting,
# not the English metadata or prose. No source JAR is needed to rebuild this pack.
JADE_ORIGINAL_JA_SHA256 = '381f227a22a7eb5cbf69c864752bd4fe72ea00f77ceed54df6b57b48550ba6b7'
JADE_METADATA_VALUE_SHA256 = 'e3cf5492749f2d1c3f333017f1aa6094138d2b02cd308c41432e25e2c51ad89a'


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


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def validate_evidence(raw, namespace, language, language_sha256):
    evidence = parse(raw)
    require(isinstance(evidence, dict) and set(evidence) == {
        'schema_version', 'namespace', 'source', 'language_sha256', 'reviews',
    } and type(evidence['schema_version']) is int and evidence['schema_version'] == 1, f'{namespace}: Unexpected review evidence schema')
    require(evidence['namespace'] == namespace and evidence['source'] == POLICIES[namespace],
            f'{namespace}: Review source/version/hash does not match the pinned MOD')
    require(evidence['language_sha256'] == language_sha256, f'{namespace}: Review evidence language hash mismatch')
    reviews = evidence['reviews']
    require(isinstance(reviews, list) and bool(reviews), f'{namespace}: No independent review evidence')
    accepted, seen_reviews, seen_batches = set(), set(), set()
    for review in reviews:
        require(isinstance(review, dict) and set(review) == {
            'batch_id', 'review_sha256', 'submission_sha256', 'reviewer', 'decision', 'accepted_keys',
        }, f'{namespace}: Unexpected review record schema')
        batch = review['batch_id']
        require(isinstance(batch, str) and re.fullmatch('[A-Za-z0-9_.+-]+', batch) and batch not in seen_batches,
                f'{namespace}: Invalid/duplicate review batch')
        seen_batches.add(batch)
        require(valid_hash(review['review_sha256']) and valid_hash(review['submission_sha256']),
                f'{namespace}: Missing review/submission SHA-256')
        require(review['review_sha256'] not in seen_reviews, f'{namespace}: Duplicate independent review')
        seen_reviews.add(review['review_sha256'])
        reviewer = review['reviewer']
        require(isinstance(reviewer, dict) and set(reviewer) == {'agent', 'model'} and
                all(isinstance(v, str) and v.strip() for v in reviewer.values()), f'{namespace}: Missing reviewer identity')
        require(isinstance(review['decision'], str) and review['decision'] in {'accepted', 'partial'}, f'{namespace}: Review does not accept keys')
        keys = review['accepted_keys']
        require(isinstance(keys, list) and bool(keys) and all(isinstance(k, str) for k in keys) and
                len(keys) == len(set(keys)), f'{namespace}: Invalid/duplicate accepted keys')
        require(not accepted.intersection(keys), f'{namespace}: Overlapping review key assignments')
        accepted.update(keys)
    require(accepted == set(language), f'{namespace}: Language keys must exactly match the independently accepted key union')


def validated_files(root, package='base'):
    config = PACKAGES[package]
    release_raw = read_file(root, config['release'])
    release = parse(release_raw)
    require(isinstance(release, dict) and set(release) == {'schema_version', 'version', 'review_status', 'languages'} and
            type(release['schema_version']) is int and release['schema_version'] == 3,
            'Unexpected release manifest schema')
    require(release['review_status'] == 'accepted', 'Independent language review is pending; no ZIP generated')
    require(release['version'] == VERSION, 'This builder prepares version 0.3.0; earlier releases remain immutable')
    require(isinstance(release['languages'], dict) and set(release['languages']) == set(config['namespaces']),
            f'{package}: Only the fixed package namespaces are permitted')
    directory = config['directory']
    pack_raw = read_file(root, directory + '/pack.mcmeta')
    require(json.dumps(parse(pack_raw), sort_keys=True, ensure_ascii=False) ==
            json.dumps(config['pack'], sort_keys=True, ensure_ascii=False),
            f'{package}: Pack metadata/filter differs from the fixed policy')
    files = {'pack.mcmeta': pack_raw, 'release.json': release_raw,
             'README.md': read_file(root, 'README.md'), 'NOTICE.md': read_file(root, config['notice'])}
    allowed_pack_files = {'pack.mcmeta'}
    for namespace, record in release['languages'].items():
        require(isinstance(record, dict) and set(record) == {
            'language_sha256', 'key_count', 'preserved_metadata_keys', 'review_evidence_sha256',
        }, f'{namespace}: Unexpected language release record')
        require(valid_hash(record['language_sha256']) and valid_hash(record['review_evidence_sha256']),
                f'{namespace}: Missing language/review evidence SHA-256')
        name = f'assets/{namespace}/lang/ja_jp.json'
        language_raw = read_file(root, directory + '/' + name)
        require(digest(language_raw) == record['language_sha256'], f'{namespace}: Language bytes changed after review')
        language = parse(language_raw)
        require(isinstance(language, dict) and bool(language) and all(isinstance(v, str) and v.strip() for v in language.values()),
                f'{namespace}: Every language value must be a nonempty string')
        expected_count, expected_keys_hash = KEY_SETS[namespace]
        keys_hash = digest(json.dumps(sorted(language), ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
        require(len(language) == expected_count and keys_hash == expected_keys_hash,
                f'{namespace}: All and only the exact source keys are required')
        require(type(record['key_count']) is int and record['key_count'] == len(language), f'{namespace}: Key count mismatch')
        require(record['preserved_metadata_keys'] == PRESERVED_METADATA_KEYS[namespace],
                f'{namespace}: Preserved metadata classification changed')
        if namespace == 'jei':
            require(language['_comment'] == JEI_METADATA_VALUE, 'JEI metadata must remain verbatim')
        if namespace == 'jade':
            require(language['__comment'] == 'Only for testing:', 'Jade testing metadata must remain verbatim')
            require(digest(language['jade.metadata'].encode('utf-8')) == JADE_METADATA_VALUE_SHA256,
                    'Jade functional settings must match the pinned original Japanese value')
        evidence_name = f'reviews/{namespace}.json'
        evidence_raw = read_file(root, evidence_name)
        require(digest(evidence_raw) == record['review_evidence_sha256'], f'{namespace}: Review evidence bytes changed')
        validate_evidence(evidence_raw, namespace, language, record['language_sha256'])
        files[name], files[evidence_name] = language_raw, evidence_raw
        allowed_pack_files.add(name)
    pack_files = set()
    for path in (root / directory).rglob('*'):
        require(not path.is_symlink(), 'Resource pack contains a symlink')
        if path.is_file():
            pack_files.add(str(path.relative_to(root / directory)))
    require(pack_files == allowed_pack_files, 'Unexpected file in resourcepack; refusing to include it')
    for name in config['licenses']:
        raw = read_file(root, name)
        require(digest(raw) == LICENSES[name], f'Upstream license bytes changed: {name}')
        files[name] = raw
    return release, files


def package_bytes(root, package='base'):
    release, files = validated_files(root, package)
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    return release['version'], output.getvalue()


def write_new_zip(directory, filename, raw):
    output = directory / filename
    if output.exists() or output.is_symlink():
        require(not output.is_symlink() and output.is_file() and output.read_bytes() == raw,
                'Existing release ZIP has different bytes; use a new version instead of overwriting it')
        return output
    fd, name = tempfile.mkstemp(prefix='.pack-', dir=directory)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, output)
    finally:
        temporary.unlink()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate release inputs without producing a ZIP')
    parser.add_argument('--pack', choices=('base', 'jade', 'all'), default='all', help='Which independent pack to validate/build')
    args = parser.parse_args()
    selected = tuple(PACKAGES) if args.pack == 'all' else (args.pack,)
    try:
        if args.check:
            for package in selected:
                validated_files(ROOT, package)
            print(f'RELEASE INPUTS OK: {VERSION}; {", ".join(selected)}; no ZIP generated')
            return 0
        # Validate and snapshot all selected inputs before producing any output.
        packages = [(PACKAGES[p]['filename'], package_bytes(ROOT, p)[1]) for p in selected]
        directory = ROOT / 'dist'
        require(not directory.is_symlink(), 'dist must not be a symlink')
        for filename, raw in packages:
            output = directory / filename
            if output.exists() or output.is_symlink():
                require(not output.is_symlink() and output.is_file() and output.read_bytes() == raw,
                        'Existing release ZIP differs; no selected ZIP was written')
        directory.mkdir(exist_ok=True)
        for filename, raw in packages:
            output = write_new_zip(directory, filename, raw)
            print(f'PACK OK: dist/{output.name}')
            print(f'SHA-256: {digest(raw)}')
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'BUILD REFUSED: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
