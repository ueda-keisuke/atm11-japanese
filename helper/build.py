#!/usr/bin/env python3
"""Portable reproduction of the 46-label development helper; no game launch/download/install."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
RELEASE_INPUTS_SHA256 = '3ff6fce757ff28db2cf30b2eec19cf1a1759a62e47168b6836c879199d25cc38'
HELPER_VERSION = '0.5.0-dev'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def strict(p):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(p.read_text(), object_pairs_hook=pairs)


def require(value, message):
    if not value:
        raise ValueError(message)


def relative(base, name):
    from pathlib import PurePosixPath
    require(isinstance(name, str) and bool(name), 'Expected relative file path')
    rel = PurePosixPath(name)
    require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name,
            'Unsafe relative path')
    path = base.joinpath(*rel.parts)
    require(path.resolve().is_relative_to(base.resolve()), 'File escapes package root')
    return path


def checked_package():
    package = strict(HERE / 'SOURCE_PACKAGE_FILES.json')
    require(package.get('schema_version') == 1, 'Unsupported source-package schema')
    for name, digest in package['files'].items():
        require(sha(relative(HERE, name).read_bytes()) == digest,
                'Source-package file changed: ' + name)
    release_path = HERE / 'release-inputs.json'
    require(sha(release_path.read_bytes()) == RELEASE_INPUTS_SHA256, 'Release-input manifest changed')
    release = strict(release_path)
    require(release.get('schema_version') == 2, 'Unsupported release-input schema')
    require(release.get('artifact') == f'atm11-japanese-helper-{HELPER_VERSION}.jar', 'Wrong helper artifact version')
    require(set(package['files']) == set(release['files']) | {'build.py', 'release-inputs.json', '.gitignore'},
            'Wrong source-package file set')
    for name, digest in release['files'].items():
        require(sha(relative(HERE, name).read_bytes()) == digest, 'Frozen source/evidence changed: ' + name)
    actual = {p.relative_to(HERE).as_posix() for folder in ('src', 'LICENSES', 'reviews')
              for p in (HERE / folder).rglob('*') if p.is_file()}
    expected = {name for name in release['files'] if name.split('/')[0] in ('src', 'LICENSES', 'reviews')}
    require(actual == expected, 'Unlisted or missing source/license/evidence file')
    evidence = strict(HERE / 'translation-evidence.json')
    require(evidence.get('schema_version') == 2
            and set(evidence['contributions']) == {'quarryplus', 'mininggadgets', 'measurements'},
            'Wrong feature evidence')
    identities = {
        'quarryplus': ('helper-quarryplus-gui-0001', 'localization/helper-mod/language-contract.json', 9),
        'mininggadgets': ('helper-mininggadgets-precision-0001', 'localization/helper-0.2-candidate/mining-language-contract.json', 2),
        'measurements': ('helper-measurements-enums-0001',
                         'localization/helper-0.3-candidate/measurements-language-contract.json', 35),
    }
    contracts, english, japanese = {}, {}, {}
    for feature, contribution in evidence['contributions'].items():
        batch_id, original_contract, count = identities[feature]
        values = {}
        for kind in ('contract', 'submission', 'review'):
            row = contribution[kind]
            path = relative(HERE, row['path'])
            require(sha(path.read_bytes()) == row['sha256'], feature + ': ' + kind + ' changed')
            values[kind] = strict(path)
        contract, submission, review = (values[k] for k in ('contract', 'submission', 'review'))
        if feature == 'measurements':
            require(contract.get('batch_id') == 'helper-measurements-enums-0001', 'Wrong Measurements batch')
            require(contract.get('source_jar_sha256') and contract.get('consumer'),
                    'Measurements source/JVM contract is incomplete')
        keys = {row['key'] for row in contract['english_contract']}
        require(len(keys) == len(contract['english_contract']) == count, 'Wrong contract key set')
        require(not keys.intersection(english), 'Feature key collision')
        require(submission.get('schema_version') == review.get('schema_version') == 1, 'Unsupported translation evidence schema')
        require(submission.get('batch_id') == review.get('batch_id') == batch_id, 'Wrong translation batch')
        require(submission.get('source') == original_contract, 'Wrong original contract reference')
        require(submission.get('source_sha256') == review.get('source_sha256') == contribution['contract']['sha256'], 'Contract identity mismatch')
        require(review.get('submission') == contribution['submission']['original_reference']
                and review.get('submission_sha256') == contribution['submission']['sha256'], 'Stale/foreign review')
        require(submission.get('locale') == 'ja_jp' and isinstance(submission.get('entries'), dict)
                and set(submission['entries']) == keys, 'Unexpected translation locale/keys')
        require(review.get('decision') == 'accepted' and review.get('issues') == [], 'Translation not fully accepted')
        for field, record in [('accepted_keys', review), ('reviewedKeys', submission)]:
            require(isinstance(record.get(field), list) and len(record[field]) == count and set(record[field]) == keys, 'Incomplete/duplicate reviewed key set')
        for who in (submission.get('worker'), review.get('reviewer')):
            require(isinstance(who, dict) and all(isinstance(who.get(k), str) and who[k].strip() for k in ('agent', 'model')), 'Missing author/reviewer identity')
        require(submission['worker']['agent'] != review['reviewer']['agent'], 'Review is not independent')
        require(isinstance(review.get('notes'), list) and review['notes']
                and all(isinstance(n, str) and n.strip() for n in review['notes']), 'Missing review notes')
        source = {row['key']: row['en_us'] for row in contract['english_contract']}
        for key, value in submission['entries'].items():
            require(isinstance(value, str) and value and value == value.strip(), 'Invalid label value')
            require(not any(c in value for c in ('\n', '\r', '{', '}', '%', '§')), 'Unexpected label formatting')
            require(all(value.count(c) == source[key].count(c) for c in ('+', '-')), 'Button sign changed')
        english.update(source)
        japanese.update(submission['entries'])
        contracts[feature] = contract
    require(len(english) == len(japanese) == 46, 'Expected exactly forty-six labels')
    expected_assets = {f'src/main/resources/assets/atm11_japanese_helper/lang/{locale}.json' for locale in ('en_us', 'ja_jp')}
    require(set(evidence['assets']) == expected_assets, 'Wrong asset set')
    for name, digest in evidence['assets'].items():
        path = relative(HERE, name)
        require(sha(path.read_bytes()) == digest, 'Language asset changed: ' + name)
        require(strict(path) == (japanese if path.name == 'ja_jp.json' else english), 'Asset differs from accepted values')
    return release, contracts


def check_measurements_runtime(contract, libraries):
    consumer = contract['consumer']
    required = {
        consumer['class']: consumer['class_sha256'],
        consumer['interface']: consumer['interface_sha256'],
    }
    neoforge = next((p for p in libraries if p.name == 'neoforge-26.1.2.106-universal.jar'), None)
    require(neoforge is not None, 'Pinned NeoForge universal JAR is required for Measurements API guard')
    observed = {}
    with zipfile.ZipFile(neoforge) as archive:
        for name, expected in required.items():
            member = name.replace('.', '/') + '.class'
            require(archive.namelist().count(member) == 1, 'Missing/duplicate Measurements runtime class: ' + name)
            actual = sha(archive.read(member))
            require(actual == expected, 'Measurements runtime class SHA256 differs: ' + name)
            observed[name] = actual
    return {'neoforge_universal_jar_sha256': sha(neoforge.read_bytes()), 'classes': observed}


def check_generation_runtime(libraries):
    contract = strict(HERE / 'neoforge-repair-contract.json')
    require(contract.get('schema_version') == 1 and contract.get('kind') == 'consumer_argument_repair_no_new_translation_keys',
            'Wrong GenerationBar repair contract')
    neoforge = next((p for p in libraries if p.name == 'neoforge-26.1.2.106-universal.jar'), None)
    require(neoforge is not None and sha(neoforge.read_bytes()) == contract['runtime_jar_sha256'],
            'GenerationBar pinned runtime JAR required')
    with zipfile.ZipFile(neoforge) as archive:
        for name, expected in contract['classes'].items():
            require(archive.namelist().count(name) == 1 and sha(archive.read(name)) == expected,
                    'GenerationBar runtime class changed: ' + name)
        language = contract['language_source']
        require(archive.namelist().count(language['entry']) == 1, 'Missing or duplicate NeoForge language entry')
        raw = archive.read(language['entry'])
        require(sha(raw) == language['sha256'], 'NeoForge English language source changed')
        require(contract['source_key'] == language['key'] and language['printf_arguments'] == ['%1$s']
                and json.loads(raw)[language['key']] == language['english_value'] == '(%1$s errors!)',
                'GenerationBar English argument contract changed')
    return {'runtime_jar_sha256': contract['runtime_jar_sha256'], 'classes': contract['classes'],
            'english_contract': language, 'runtime_guard_scope': 'Consumer class hashes and callsite shape; English asset checked separately at build time.'}


def check_fluix_runtime(contract, libraries, ae2):
    """Pin the optional AE2/Minecraft consumer pair and the five fixed recipes."""
    require(contract.get('schema_version') == 1, 'Unsupported Fluix repair contract')
    require(contract.get('kind') == 'consumer_component_repair_no_new_translation_keys',
            'Wrong Fluix repair contract')
    require(sha(ae2.read_bytes()) == contract['source_jar_sha256'],
            'Applied Energistics 2 JAR SHA256 differs')
    classes = contract.get('classes')
    require(isinstance(classes, dict) and len(classes) == 2,
            'Fluix contract must bind exactly two production classes')
    observed = {}
    with zipfile.ZipFile(ae2) as archive:
        ae2_classes = {name: expected for name, expected in classes.items() if name.startswith('appeng/')}
        require(len(ae2_classes) == 1, 'Fluix contract must bind one AE2 target class')
        for member, expected in ae2_classes.items():
            require(archive.namelist().count(member) == 1,
                    'Missing/duplicate AE2 runtime class: ' + member)
            actual = sha(archive.read(member))
            require(actual == expected, 'AE2 runtime class SHA256 differs: ' + member)
            observed[member] = actual
        for locale, row in contract['language_sources'].items():
            require(archive.namelist().count(row['entry']) == 1,
                    'Missing/duplicate AE2 language source: ' + locale)
            require(sha(archive.read(row['entry'])) == row['sha256'],
                    'AE2 language source SHA256 differs: ' + locale)
        recipe_observed = []
        for recipe in contract['recipes']:
            require(archive.namelist().count(recipe['entry']) == 1,
                    'Missing/duplicate AE2 Fluix recipe: ' + recipe['entry'])
            raw = archive.read(recipe['entry'])
            require(sha(raw) == recipe['sha256'], 'AE2 recipe SHA256 differs: ' + recipe['entry'])
            payload = json.loads(raw)
            require(payload.get('type') == recipe['type'], 'AE2 recipe type differs: ' + recipe['entry'])
            def ingredient(field):
                value = payload.get(field)
                if isinstance(value, dict):
                    if 'item' in value:
                        return value['item']
                    if 'tag' in value:
                        return '#' + value['tag']
                return value
            require(ingredient('template') == recipe['template']
                    and ingredient('addition') == recipe['addition']
                    and ingredient('base') == recipe['base'],
                    'AE2 recipe ingredient contract differs: ' + recipe['entry'])
            result = payload.get('result')
            result_id = result.get('id') if isinstance(result, dict) else result
            require(result_id == recipe['result_id'], 'AE2 recipe result contract differs: ' + recipe['entry'])
            recipe_observed.append(recipe['result_id'])
    runtime_jar = next((p for p in libraries if p.name == contract['minecraft_runtime_jar']), None)
    require(runtime_jar is not None and sha(runtime_jar.read_bytes()) == contract['minecraft_runtime_jar_sha256'],
            'Pinned Minecraft runtime JAR required for Fluix consumer guard')
    mc_members = {name: expected for name, expected in classes.items() if name.startswith('net/')}
    require(len(mc_members) == 1, 'Fluix contract must bind one Minecraft superclass')
    with zipfile.ZipFile(runtime_jar) as archive:
        for member, expected in mc_members.items():
            require(archive.namelist().count(member) == 1 and sha(archive.read(member)) == expected,
                    'Minecraft consumer class SHA256 differs: ' + member)
            observed[member] = expected
    recipes = contract.get('recipes')
    require(isinstance(recipes, list) and len(recipes) == 5, 'Fluix contract must bind five recipes')
    require(len(set(recipe_observed)) == 5 and all(x.startswith('ae2:fluix_') for x in recipe_observed),
            'Fluix recipes must be five distinct AE2 Fluix tools')
    return {'ae2_jar_sha256': contract['source_jar_sha256'], 'classes': observed,
            'minecraft_runtime_jar': contract['minecraft_runtime_jar'],
            'minecraft_runtime_jar_sha256': contract['minecraft_runtime_jar_sha256'],
            'source_commit': contract['source_commit'], 'language_sources': contract['language_sources'],
            'recipes': recipe_observed,
            'runtime_scope': 'AE2 Fluix template consumer and fixed five recipe additions; no new language keys. Recipe and language SHA checks are build/verification checks and do not monitor runtime datapack reloads.'}


def checked_inputs(prism, quarry, mining, measurements, ae2, java_home=None):
    release, contracts = checked_package()
    for feature, jar in (('quarryplus', quarry), ('mininggadgets', mining), ('measurements', measurements)):
        contract = contracts[feature]
        require(jar.is_file(), 'Specify the separately obtained original JAR: ' + feature)
        require(sha(jar.read_bytes()) == contract['source_jar_sha256'], feature + ' JAR SHA256 differs')
        with zipfile.ZipFile(jar) as archive:
            expected_classes = {}
            for row in contract['english_contract']:
                expected_classes[row['target_class']] = row['target_class_sha256']
            if feature == 'measurements':
                require(len(expected_classes) == 2, 'Measurements contract must bind exactly two enum classes')
            for target_class, target_sha in expected_classes.items():
                member = target_class.replace('.', '/') + '.class'
                require(archive.namelist().count(member) == 1, 'Missing/duplicate target class')
                require(sha(archive.read(member)) == target_sha, 'Target class SHA256 differs: ' + target_class)
    lock = strict(HERE / 'dependencies.lock.json')
    libraries = []
    for row in lock['libraries']:
        path = relative(prism / 'libraries', row['path'])
        require(path.is_file(), 'Missing Prism dependency: ' + row['path'])
        require(sha(path.read_bytes()) == row['sha256'], 'Prism dependency changed: ' + row['path'])
        libraries.append(path)
    if java_home is None:
        reference = prism / 'java/java-runtime-epsilon/jre.bundle/Contents/Home'
        require(reference.is_dir(), 'Specify your JDK 25.0.1 installation with --java-home')
        java_home = reference
    java = java_home / 'bin'
    executable = 'javac.exe' if os.name == 'nt' else 'javac'
    version = subprocess.check_output([str(java / executable), '-version'], text=True).strip()
    require(version == lock['javac_version'], 'Pinned compiler version required: ' + lock['javac_version'])
    observed = {}
    for name in lock['jdk_files']:
        path = java_home / name
        if not path.is_file() and path.suffix == '' and os.name == 'nt' and name.startswith('bin/'):
            path = path.with_suffix('.exe')
        observed[name] = sha(path.read_bytes()) if path.is_file() else None
    toolchain = {'javac': version, 'jdk_file_sha256': observed,
                 'matches_reference_jdk': observed == lock['jdk_files'],
                 'acceptance': 'Final JAR SHA256 must match the frozen reference regardless of toolchain platform.'}
    runtime = check_measurements_runtime(contracts['measurements'], libraries)
    generation_runtime = check_generation_runtime(libraries)
    fluix_contract = strict(HERE / 'fluix-repair-contract.json')
    fluix_runtime = check_fluix_runtime(fluix_contract, libraries, ae2)
    return java, libraries, quarry, mining, measurements, version, toolchain, runtime, generation_runtime, ae2, fluix_runtime


def jar_bytes(classes):
    import io
    output = io.BytesIO()
    entries = {'META-INF/MANIFEST.MF': f'Manifest-Version: 1.0\r\nImplementation-Version: {HELPER_VERSION}\r\n\r\n'.encode()}
    for base in (classes, HERE / 'src/main/resources'):
        for p in sorted(base.rglob('*')):
            if p.is_file():
                key = p.relative_to(base).as_posix()
                if key in entries:
                    raise ValueError('Duplicate JAR member: ' + key)
                entries[key] = p.read_bytes()
    for p in sorted((HERE / 'LICENSES').glob('*.txt')):
        entries['LICENSES/' + p.name] = p.read_bytes()
    entries['NOTICE.md'] = (HERE / 'NOTICE.md').read_bytes()
    expected = {'META-INF/MANIFEST.MF', 'META-INF/neoforge.mods.toml', 'NOTICE.md',
                'LICENSES/LGPL-3.0.txt', 'LICENSES/GPL-3.0.txt', 'LICENSES/MiningGadgets-MIT.txt',
                'LICENSES/Measurements-MIT.txt', 'LICENSES/NeoForge-LGPL-2.1.txt',
                'atm11_japanese_helper.mixins.json', 'atm11_japanese_helper.mining.mixins.json',
                'atm11_japanese_helper.measurements.mixins.json', 'atm11_japanese_helper.neoforge.mixins.json',
                'assets/atm11_japanese_helper/lang/en_us.json', 'assets/atm11_japanese_helper/lang/ja_jp.json'}
    expected.update('dev/atm11/japanesehelper/' + name + '.class' for name in (
            'JapaneseHelper', 'Labels', 'ExactQuarryGuard', 'ExactMiningGuard', 'ExactMeasurementsGuard', 'ExactGenerationGuard', 'mixin/GenerationBarMixin',
            'ExactFluixGuard', 'mixin/FluixTemplateMixin', 'mixin/MiningSettingScreenMixin', 'mixin/ChunkMarkerScreenMixin', 'mixin/ModuleScreenMixin',
            'mixin/PlacerScreenMixin', 'mixin/MeasurementsLineColorMixin', 'mixin/MeasurementsTextColorMixin'))
    expected.add('atm11_japanese_helper.ae2.fluix.mixins.json')
    if set(entries) != expected:
        raise ValueError('Unexpected or missing helper JAR members: ' + str(set(entries) ^ expected))
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as z:
        for key, raw in sorted(entries.items()):
            info = zipfile.ZipInfo(key, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prism-root', type=Path, required=True, help='Existing PrismLauncher data directory containing libraries/')
    parser.add_argument('--quarry-jar', type=Path, required=True, help='Original QuarryPlus 26.12.160 JAR obtained separately')
    parser.add_argument('--mining-jar', type=Path, required=True, help='Original Mining Gadgets 1.19.3 JAR obtained separately')
    parser.add_argument('--measurements-jar', type=Path, required=True, help='Original Measurements 4.0.0 JAR obtained separately')
    parser.add_argument('--ae2-jar', type=Path, required=True, help='Original Applied Energistics 2 26.1.10-beta JAR obtained separately')
    parser.add_argument('--java-home', type=Path, help='Existing JDK 25.0.1 home (needed outside reference macOS layout)')
    parser.add_argument('--verify', action='store_true', help='Run the offline real-Mixin transform harness after building')
    parser.add_argument('--language-pack', type=Path, help='Separately downloaded ATM11-Japanese-0.24.0.zip; required with --verify')
    args = parser.parse_args()
    if args.verify and args.language_pack is None:
        parser.error('--verify requires --language-pack for accepted Japanese consumer fixtures')
    java, libraries, quarry, mining, measurements, version, toolchain, runtime, generation_runtime, ae2, fluix_runtime = checked_inputs(
        args.prism_root.resolve(), args.quarry_jar.resolve(), args.mining_jar.resolve(),
        args.measurements_jar.resolve(), args.ae2_jar.resolve(), args.java_home.resolve() if args.java_home else None)
    build = HERE / 'build'
    build.mkdir(exist_ok=True)
    classes = build / 'classes'
    if classes.exists():
        shutil.rmtree(classes)
    classes.mkdir()
    cp = os.pathsep.join(map(str, libraries))
    sources = sorted((HERE / 'src/main/java').rglob('*.java'))
    subprocess.run([str(java / ('javac.exe' if os.name == 'nt' else 'javac')), '--release', '25', '-encoding', 'UTF-8', '-proc:none', '-g:none',
                    '-classpath', cp, '-d', str(classes), *map(str, sources)], check=True, cwd=build)
    raw = jar_bytes(classes)
    release = strict(HERE / 'release-inputs.json')
    require(sha(raw) == release['artifact_sha256'], 'Output differs from frozen reference; do not publish/install it')
    jar = build / release['artifact']
    jar.write_bytes(raw)
    report = {'schema_version': 2, 'artifact': jar.name, 'version': HELPER_VERSION, 'sha256': sha(raw), 'javac': version,
              'translation_evidence_sha256': sha((HERE / 'translation-evidence.json').read_bytes()),
              'dependencies_lock_sha256': sha((HERE / 'dependencies.lock.json').read_bytes()),
              'measurements_contract_sha256': sha((HERE / 'measurements-language-contract.json').read_bytes()),
              'measurements_jar_sha256': sha(measurements.read_bytes()),
              'measurements_runtime_guards': runtime,
              'generation_repair_runtime_contract': generation_runtime,
              'ae2_jar_sha256': sha(ae2.read_bytes()),
              'fluix_runtime_guards': fluix_runtime,
              'label_count': 46,
              'source_files': {p.relative_to(HERE).as_posix(): sha(p.read_bytes())
                               for base in ('src', 'LICENSES') for p in sorted((HERE / base).rglob('*')) if p.is_file()},
              'toolchain': toolchain, 'matches_frozen_binary': True, 'installed': False, 'in_game_visual_qa': False}
    (build / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('BUILT', jar.name, sha(raw))
    if args.verify:
        command = [sys.executable, str(HERE / 'verify.py'), '--prism-root', str(args.prism_root.resolve()),
                   '--quarry-jar', str(args.quarry_jar.resolve()), '--mining-jar', str(args.mining_jar.resolve()),
                   '--measurements-jar', str(args.measurements_jar.resolve()),
                   '--ae2-jar', str(args.ae2_jar.resolve()),
                   '--language-pack', str(args.language_pack.resolve())]
        if args.java_home:
            command += ['--java-home', str(args.java_home.resolve())]
        subprocess.run(command, check=True, cwd=build)


if __name__ == '__main__':
    main()
