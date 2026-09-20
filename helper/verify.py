#!/usr/bin/env python3
"""Apply the actual Mixin engine to upstream class bytes without starting Minecraft."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from build import HERE, checked_inputs, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prism-root', type=Path, required=True)
    parser.add_argument('--quarry-jar', type=Path, required=True)
    parser.add_argument('--mining-jar', type=Path, required=True)
    parser.add_argument('--java-home', type=Path)
    args = parser.parse_args()
    java, libraries, quarry, mining, version, toolchain = checked_inputs(args.prism_root.resolve(), args.quarry_jar.resolve(), args.mining_jar.resolve(), args.java_home.resolve() if args.java_home else None)
    build = HERE / 'build'
    jar = build / 'atm11-japanese-helper-0.2.0-dev.jar'
    if not jar.is_file():
        raise ValueError('Run build.py first')
    report = json.loads((build / 'build-report.json').read_text())
    if sha(jar.read_bytes()) != report['sha256']:
        raise ValueError('Built helper JAR changed')
    for relative, expected in report['source_files'].items():
        if sha((HERE / relative).read_bytes()) != expected:
            raise ValueError('Source changed after build: ' + relative)
    if sha((HERE / 'dependencies.lock.json').read_bytes()) != report['dependencies_lock_sha256']:
        raise ValueError('Dependency lock changed after build')
    test_classes = build / 'test-classes'
    if test_classes.exists():
        shutil.rmtree(test_classes)
    test_classes.mkdir()
    compile_cp = os.pathsep.join(map(str, [jar, *libraries]))
    subprocess.run([str(java / ('javac.exe' if os.name == 'nt' else 'javac')), '--release', '25', '-encoding', 'UTF-8', '-proc:none',
                    '-classpath', compile_cp, '-d', str(test_classes),
                    *map(str, sorted((HERE / 'src/test/java').rglob('*.java')))], check=True, cwd=build)
    shutil.copytree(HERE / 'src/test/resources', test_classes, dirs_exist_ok=True)
    cp = os.pathsep.join(map(str, [test_classes, jar, quarry, mining, *libraries]))
    flags = ['-Datm11.helper.offline=true', '-Dmixin.service=helpertest.OfflineMixinService',
             '-Dmixin.env.disableRefMap=true']
    def run(name, main, extra=(), classpath=cp, expected_error=None):
        command = [str(java / ('java.exe' if os.name == 'nt' else 'java')), *flags, '-cp', classpath, main, *map(str, extra)]
        result = subprocess.run(command, cwd=build, capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        # Generated local diagnostics retain no host-specific absolute paths.
        from urllib.parse import quote
        for local, label in ((HERE, '<SOURCE_ROOT>'), (args.prism_root.resolve(), '<PRISM_ROOT>'),
                             (quarry, '<QUARRY_JAR>'), (mining, '<MINING_JAR>'), (java.parent, '<JAVA_HOME>')):
            output = output.replace(quote(str(local)), label).replace(str(local), label)
        (build / (name + '.log')).write_text(output)
        if expected_error:
            if not result.returncode or expected_error not in output:
                print(output)
                raise ValueError('Expected specific rejection: ' + name)
            print('PASS rejected:', name)
        else:
            print('\n'.join(line for line in output.splitlines() if line.startswith('PASS ')))
            if result.returncode:
                print(output)
                raise SystemExit(result.returncode)
        return {'exit_code': result.returncode, 'log_sha256': sha(output.encode()), 'expected_failure': bool(expected_error)}

    inputs = {str(p): sha(p.read_bytes()) for p in [jar, quarry, mining, *libraries]}
    results = {}
    results['transform'] = run('transform', 'helpertest.TransformHarness', [build / 'transformed'])
    transform_log = (build / 'transform.log').read_text()
    if transform_log.count('ATM11_JAPANESE_HELPER_SOURCE_OK:') != 1 or transform_log.count('ATM11_JAPANESE_HELPER_APPLIED target=') != 3:
        raise ValueError('Runtime diagnostic distinction is missing')
    results['language'] = run('language', 'helpertest.LanguageHarness')
    results['missing-injection-site'] = run('missing-injection-site', 'helpertest.TransformHarness',
            [build / 'fixture-missing-site', 'missing-site'], expected_error='InvalidInjectionException')
    fixture = build / 'fixture-changed-class'
    fixture.mkdir(exist_ok=True)
    member = 'com/yogpc/qp/machine/marker/ChunkMarkerScreen.class'
    with zipfile.ZipFile(quarry) as archive:
        original = archive.read(member)
    if original.count(b'\x00\x04Size') != 1:
        raise ValueError('Unexpected fixture constant-pool layout')
    altered = original.replace(b'\x00\x04Size', b'\x00\x04SIZE')
    target = fixture / member
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(altered)
    results['changed-upstream-class'] = run('changed-upstream-class', 'helpertest.TransformHarness',
            [build / 'fixture-rejected', 'unsupported'], classpath=str(fixture) + os.pathsep + cp)
    if 'UNSUPPORTED: ATM11 Japanese Helper supports only the pinned QuarryPlus' not in (build / 'changed-upstream-class.log').read_text():
        raise ValueError('Missing clear unsupported-source diagnostic')
    if 'ATM11_JAPANESE_HELPER_APPLIED target=' in (build / 'changed-upstream-class.log').read_text():
        raise ValueError('Unsupported source must not report any applied target')
    mining_config = 'atm11_japanese_helper.mining.mixins.json'
    results['mining-transform'] = run('mining-transform', 'helpertest.MiningTransformHarness',
            [build / 'mining-transformed', mining_config])
    mining_class = build / 'mining-transformed/com/direwolf20/mininggadgets/client/screens/MiningSettingScreen.class'
    results['mining-language'] = run('mining-language', 'helpertest.MiningLanguageHarness',
            [mining_class, HERE / 'reviews/mining-submission.json'])
    results['mining-missing-site'] = run('mining-missing-site', 'helpertest.MiningTransformHarness',
            [build / 'mining-missing-site', mining_config, 'missing-site'], expected_error='Mining precision consumer shape changed before transformation')
    mining_fixture = build / 'fixture-changed-mining'
    mining_member = 'com/direwolf20/mininggadgets/client/screens/MiningSettingScreen.class'
    with zipfile.ZipFile(mining) as archive:
        original_mining = archive.read(mining_member)
    require_pattern = b'tooltip.screen.precision_mode'
    if original_mining.count(require_pattern) != 1:
        raise ValueError('Unexpected Mining class constant pool')
    modified_mining = original_mining.replace(require_pattern, b'tooltip.screen.precision_modX')
    mining_target = mining_fixture / mining_member
    mining_target.parent.mkdir(parents=True, exist_ok=True)
    mining_target.write_bytes(modified_mining)
    modes = {
        'both': [quarry, mining],
        'mining-absent': [quarry],
        'mining-mismatch': [mining_fixture, quarry, mining],
        'quarry-absent': [mining],
        'quarry-mismatch': [fixture, quarry, mining],
        'both-absent': [],
    }
    for mode, feature_paths in modes.items():
        feature_cp = os.pathsep.join(map(str, [test_classes, jar, *feature_paths, *libraries]))
        results['guard-' + mode] = run('guard-' + mode, 'helpertest.GuardIsolationHarness',
                [build / ('guard-' + mode), mode], classpath=feature_cp)
        guard_log = (build / ('guard-' + mode + '.log')).read_text()
        quarry_expected = mode in ('both', 'mining-absent', 'mining-mismatch')
        mining_expected = mode in ('both', 'quarry-absent', 'quarry-mismatch')
        if guard_log.count('ATM11_JAPANESE_HELPER_APPLIED target=') != (3 if quarry_expected else 0):
            raise ValueError('Quarry applied diagnostics differ for ' + mode)
        if guard_log.count('ATM11_JAPANESE_HELPER_MINING_APPLIED target=') != (1 if mining_expected else 0):
            raise ValueError('Mining applied diagnostics differ for ' + mode)
        if not quarry_expected and 'UNSUPPORTED: ATM11 Japanese Helper supports only the pinned QuarryPlus' not in guard_log:
            raise ValueError('Missing Quarry unsupported diagnostic')
        if not mining_expected and 'UNSUPPORTED Mining Gadgets:' not in guard_log:
            raise ValueError('Missing Mining unsupported diagnostic')
    for path, digest in inputs.items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Verification input changed: ' + path)
    for relative, expected in report['source_files'].items():
        if sha((HERE / relative).read_bytes()) != expected:
            raise ValueError('Source changed during verification: ' + relative)
    summary = {'schema_version': 2, 'helper_sha256': sha(jar.read_bytes()), 'results': results,
               'independently_reviewed_helper_labels': 11, 'quarry_label_injection_sites': 12,
               'mining_precision_injection_sites': 2, 'optional_feature_isolation_modes': list(modes),
               'input_files_unchanged': True,

               'quarry_jar_sha256': sha(quarry.read_bytes()), 'mining_jar_sha256': sha(mining.read_bytes()), 'no_game_launch': True,
               'no_installation': True, 'visual_qa': False}
    (build / 'verification-report.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    main()
