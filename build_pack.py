#!/usr/bin/env python3
"""Build the reviewed Transmog + JEI overlay from pinned release evidence."""
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
TRANSMOG_KEYS = {
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
    'pack': {'description': 'ATM11 日本語改善: Transmog / JEI',
             'min_format': [84, 0], 'max_format': [84, 0]},
    'filter': {'block': [{'namespace': '^transmog$', 'path': r'^lang/ja_jp\.json$'}]},
}
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
}
LICENSES = {
    'LICENSES/Transmog-MIT.txt': 'a366506974a46752dbf54c187288b5d5de7f4570422b0cbacd4f5cd1dcb8f099',
    'LICENSES/JEI-MIT.txt': '108c93a97f3011c196b8226f5019a9c09ade318fe3a802be2f7f5ddb2c3a0d04',
}
JEI_METADATA_VALUE = 'Debug (for a debug mode, do not need translation)'


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


def validated_files(root):
    release_raw = read_file(root, 'release.json')
    release = parse(release_raw)
    require(isinstance(release, dict) and set(release) == {'schema_version', 'version', 'review_status', 'languages'} and
            type(release['schema_version']) is int and release['schema_version'] == 2,
            'Unexpected release.json schema')
    require(release['review_status'] == 'accepted', 'Independent language review is pending; no ZIP generated')
    require(release['version'] == '0.2.0', 'This builder prepares version 0.2.0; earlier releases remain immutable')
    require(isinstance(release['languages'], dict) and set(release['languages']) == set(POLICIES), 'Only Transmog and JEI are permitted')
    pack_raw = read_file(root, 'resourcepack/pack.mcmeta')
    require(parse(pack_raw) == EXPECTED_PACK, 'Only pack format 84.0 and the exact Transmog language filter are permitted')
    files = {'pack.mcmeta': pack_raw, 'release.json': release_raw,
             'README.md': read_file(root, 'README.md'), 'NOTICE.md': read_file(root, 'NOTICE.md')}
    allowed_pack_files = {'pack.mcmeta'}
    for namespace, record in release['languages'].items():
        require(isinstance(record, dict) and set(record) == {
            'language_sha256', 'key_count', 'display_key_count', 'review_evidence_sha256',
        }, f'{namespace}: Unexpected language release record')
        require(valid_hash(record['language_sha256']) and valid_hash(record['review_evidence_sha256']),
                f'{namespace}: Missing language/review evidence SHA-256')
        name = f'assets/{namespace}/lang/ja_jp.json'
        language_raw = read_file(root, 'resourcepack/' + name)
        require(digest(language_raw) == record['language_sha256'], f'{namespace}: Language bytes changed after review')
        language = parse(language_raw)
        require(isinstance(language, dict) and bool(language) and all(isinstance(v, str) and v.strip() for v in language.values()),
                f'{namespace}: Every translation must be a nonempty string')
        require(type(record['key_count']) is int and record['key_count'] == len(language), f'{namespace}: Key count mismatch')
        display_count = len(language) - ('_comment' in language)
        require(type(record['display_key_count']) is int and record['display_key_count'] == display_count and display_count > 0,
                f'{namespace}: Display-key count mismatch')
        if namespace == 'transmog':
            require(set(language) == TRANSMOG_KEYS, 'All and only the 25 Transmog keys are required')
        else:
            require(len(language) <= 335 and all(k == '_comment' or re.fullmatch(
                r'(?:description\.jei\.|gui\.jei\.|jei\.|key\.(?:category\.)?jei\.)[A-Za-z0-9_.-]+', k) for k in language),
                    'JEI language includes keys outside the known namespace or source size')
            require('_comment' not in language or language['_comment'] == JEI_METADATA_VALUE, 'JEI metadata must remain verbatim')
        evidence_name = f'reviews/{namespace}.json'
        evidence_raw = read_file(root, evidence_name)
        require(digest(evidence_raw) == record['review_evidence_sha256'], f'{namespace}: Review evidence bytes changed')
        validate_evidence(evidence_raw, namespace, language, record['language_sha256'])
        files[name], files[evidence_name] = language_raw, evidence_raw
        allowed_pack_files.add(name)
    pack_files = set()
    for path in (root / 'resourcepack').rglob('*'):
        require(not path.is_symlink(), 'Resource pack contains a symlink')
        if path.is_file():
            pack_files.add(str(path.relative_to(root / 'resourcepack')))
    require(pack_files == allowed_pack_files, 'Unexpected file in resourcepack; refusing to include it')
    for name, expected_hash in LICENSES.items():
        raw = read_file(root, name)
        require(digest(raw) == expected_hash, f'Upstream MIT license bytes changed: {name}')
        files[name] = raw
    return release, files


def package_bytes(root):
    release, files = validated_files(root)
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate release inputs without producing a ZIP')
    args = parser.parse_args()
    try:
        if args.check:
            release, _ = validated_files(ROOT)
            print(f'RELEASE INPUTS OK: {release["version"]}; no ZIP generated')
            return 0
        version, raw = package_bytes(ROOT)
        directory = ROOT / 'dist'
        require(not directory.is_symlink(), 'dist must not be a symlink')
        directory.mkdir(exist_ok=True)
        output = directory / f'ATM11-Japanese-{version}.zip'
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
