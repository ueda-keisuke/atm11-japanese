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
from build import HERE, checked_inputs, checked_package, sha


def strict_bytes(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs)


def measurements_language_checks(jar):
    """Validate the exact 35-key derived language surface and no feature collision."""
    contract = json.loads((HERE / 'measurements-language-contract.json').read_text())
    expected = {row['key']: row['en_us'] for row in contract['english_contract']}
    def require(ok, message):
        if not ok:
            raise ValueError(message)
    with zipfile.ZipFile(jar) as archive:
        en = strict_bytes(archive.read('assets/atm11_japanese_helper/lang/en_us.json'))
        ja = strict_bytes(archive.read('assets/atm11_japanese_helper/lang/ja_jp.json'))
    require(set(expected).issubset(en) and set(expected).issubset(ja),
            'Measurements language keys missing from built assets')
    require(all(en[key] == value for key, value in expected.items()),
            'Measurements English contract differs from built asset')
    require(all(isinstance(ja[key], str) and ja[key].strip() for key in expected),
            'Measurements Japanese labels contain an empty value')
    evidence = json.loads((HERE / 'translation-evidence.json').read_text())
    contribution_keys = []
    for contribution in evidence['contributions'].values():
        path = HERE / contribution['contract']['path']
        contract_data = json.loads(path.read_text())
        contribution_keys.extend(row['key'] for row in contract_data['english_contract'])
    require(len(contribution_keys) == len(set(contribution_keys)) == 46,
            'Accepted helper contributions contain a key collision')
    require(set(en) == set(contribution_keys) and set(ja) == set(contribution_keys),
            'Built helper assets are not the exact 46-key set')
    return {
        'english_key_count': len(en),
        'japanese_key_count': len(ja),
        'measurements_key_count': len(expected),
        'measurements_english_contract_match': True,
        'measurements_japanese_nonempty': True,
        'feature_key_collision': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prism-root', type=Path, required=True)
    parser.add_argument('--quarry-jar', type=Path, required=True)
    parser.add_argument('--mining-jar', type=Path, required=True)
    parser.add_argument('--measurements-jar', type=Path, required=True)
    parser.add_argument('--java-home', type=Path)
    parser.add_argument('--language-pack', type=Path, required=True)
    args = parser.parse_args()
    java, libraries, quarry, mining, measurements, version, toolchain, measurements_runtime, generation_runtime = checked_inputs(
        args.prism_root.resolve(), args.quarry_jar.resolve(), args.mining_jar.resolve(),
        args.measurements_jar.resolve(), args.java_home.resolve() if args.java_home else None)
    build = HERE / 'build'
    repair = json.loads((HERE / 'neoforge-repair-contract.json').read_bytes())
    overlay = args.language_pack.resolve()
    if sha(overlay.read_bytes()) != repair['verification_overlay']['sha256']:
        raise ValueError('Expected the separately obtained, fixed public Japanese language pack')
    neoforge = next(p for p in libraries if p.name == 'neoforge-26.1.2.106-universal.jar')
    release_inputs = json.loads((HERE / 'release-inputs.json').read_text())
    jar = build / release_inputs['artifact']
    if not jar.is_file():
        raise ValueError('Run build.py first')
    report = json.loads((build / 'build-report.json').read_text())
    if sha(jar.read_bytes()) != report['sha256'] or report['sha256'] != release_inputs['artifact_sha256']:
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
    def run(name, main, extra=(), classpath=cp, expected_error=None, jvm_args=()):
        command = [str(java / ('java.exe' if os.name == 'nt' else 'java')), *flags, *jvm_args, '-cp', classpath, main, *map(str, extra)]
        result = subprocess.run(command, cwd=build, capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        # Generated local diagnostics retain no host-specific absolute paths.
        from urllib.parse import quote
        for local, label in ((HERE, '<SOURCE_ROOT>'), (build.resolve(), '<BUILD_ROOT>'),
                             (args.prism_root.resolve(), '<PRISM_ROOT>'),
                             (quarry, '<QUARRY_JAR>'), (mining, '<MINING_JAR>'),
                             (measurements, '<MEASUREMENTS_JAR>'), (overlay, '<LANGUAGE_PACK>'), (java.parent, '<JAVA_HOME>')):
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

    inputs = {str(p): sha(p.read_bytes()) for p in [jar, quarry, mining, measurements, overlay, *libraries]}
    results = {}
    results['transform'] = run('transform', 'helpertest.TransformHarness', [build / 'transformed'])
    transform_log = (build / 'transform.log').read_text()
    if transform_log.count('ATM11_JAPANESE_HELPER_SOURCE_OK:') != 1 or transform_log.count('ATM11_JAPANESE_HELPER_APPLIED target=') != 3:
        raise ValueError('Runtime diagnostic distinction is missing')
    results['language'] = run('language', 'helpertest.LanguageHarness')
    language_observation = measurements_language_checks(jar)
    measurement_cp = os.pathsep.join(map(str, [test_classes, jar, quarry, mining, measurements, *libraries]))
    results['measurements-transform'] = run('measurements-transform', 'helpertest.MeasurementsTransformHarness',
            [build / 'measurements-transformed'], classpath=measurement_cp)
    results['measurements-collision'] = run('measurements-collision', 'helpertest.MeasurementsTransformHarness',
            [build / 'measurements-method-collision', 'method-collision'], classpath=measurement_cp,
            expected_error='Measurements enum shape or display method changed before transformation')
    results['measurements-language'] = run('measurements-language', 'helpertest.MeasurementsLanguageHarness',
            [build / 'measurements-transformed', HERE / 'reviews/measurements-submission.json',
             build / 'measurements-language-report.json'], classpath=measurement_cp)
    consumer_report = strict_bytes((build / 'measurements-language-report.json').read_bytes())
    if consumer_report.get('pass') is not True:
        raise ValueError('Measurements real consumer language harness did not pass')
    results['measurements-language']['report_sha256'] = sha((build / 'measurements-language-report.json').read_bytes())
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

    measurement_fixtures = {}
    measurement_members = {
        'line-mismatch': 'com/mrbysco/measurements/config/LineColor.class',
        'text-mismatch': 'com/mrbysco/measurements/config/TextColor.class',
        'consumer-mismatch': 'net/neoforged/neoforge/client/gui/ConfigurationScreen$ConfigurationSectionScreen.class',
        'interface-mismatch': 'net/neoforged/neoforge/common/TranslatableEnum.class',
    }
    neoforge = next(p for p in libraries if p.name == 'neoforge-26.1.2.106-universal.jar')
    for mode, member in measurement_members.items():
        fixture_root = build / ('fixture-' + mode)
        fixture_target = fixture_root / member
        fixture_target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(measurements if member.startswith('com/mrbysco/') else neoforge) as archive:
            original_measurements = archive.read(member)
        source_name = member.rsplit('/', 1)[1].split('$', 1)[0].replace('.class', '') + '.java'
        pattern = source_name.encode()
        if original_measurements.count(pattern) != 1:
            raise ValueError('Unexpected source-file constant in fixture: ' + member)
        # Preserve class validity and method behavior; only the SourceFile value changes.
        altered_measurements = original_measurements.replace(pattern, pattern[:-1] + b'X')
        fixture_target.write_bytes(altered_measurements)
        measurement_fixtures[mode] = fixture_root

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

    measurements_modes = {
        'all': [quarry, mining, measurements],
        'measurements-absent': [quarry, mining],
        'line-mismatch': [quarry, mining, measurement_fixtures['line-mismatch'], measurements],
        'text-mismatch': [quarry, mining, measurement_fixtures['text-mismatch'], measurements],
        'consumer-mismatch': [quarry, mining, measurement_fixtures['consumer-mismatch'], measurements],
        'interface-mismatch': [quarry, mining, measurement_fixtures['interface-mismatch'], measurements],
        'quarry-absent': [mining, measurements],
        'quarry-mismatch': [fixture, quarry, mining, measurements],
        'mining-absent': [quarry, measurements],
        'mining-mismatch': [mining_fixture, mining, quarry, measurements],
        'all-absent': [],
    }
    for mode, feature_paths in measurements_modes.items():
        feature_cp = os.pathsep.join(map(str, [test_classes, jar, *feature_paths, *libraries]))
        result_name = 'measurements-guard-' + mode
        results[result_name] = run(result_name, 'helpertest.MeasurementsGuardHarness',
                [build / result_name, mode], classpath=feature_cp)
        report_path = build / result_name / 'measurements-guard-report.json'
        guard_report = json.loads(report_path.read_text())
        measurement_active = mode not in {'measurements-absent', 'line-mismatch', 'text-mismatch',
                                          'consumer-mismatch', 'interface-mismatch', 'all-absent'}
        quarry_active = mode not in {'quarry-absent', 'quarry-mismatch', 'all-absent'}
        mining_active = mode not in {'mining-absent', 'mining-mismatch', 'all-absent'}
        if guard_report.get('measurements_supported_expected') != measurement_active:
            raise ValueError('Measurements support expectation differs for ' + mode)
        for feature, active in (('quarry', quarry_active), ('mining', mining_active),
                                ('measurements', measurement_active)):
            feature_records = [record for record in guard_report['records'] if record['feature'] == feature]
            if feature == 'measurements':
                require_count = 2
            elif feature == 'quarry':
                require_count = 3
            else:
                require_count = 1
            if len(feature_records) != require_count:
                raise ValueError('Unexpected ' + feature + ' record count for ' + mode)
            for record in feature_records:
                expected = active and bool(record.get('resource_present_to_harness'))
                if bool(record.get('transformed')) != expected:
                    raise ValueError('Feature result differs for ' + feature + ' in ' + mode)
                if feature == 'measurements' and active and record.get('transformed'):
                    if record.get('get_translated_name_count') != 1 or not record.get('translatable_enum_interface'):
                        raise ValueError('Measurements transformed enum contract missing in ' + mode)
    generation_cp = os.pathsep.join(map(str, [test_classes, jar, *libraries]))
    generation_details = {}
    def generation_case(name, side='SERVER', mode='normal', prefix=(), jvm_args=(), expected_error=None):
        classpath = os.pathsep.join([*map(str, prefix), generation_cp])
        results[name] = run(name, 'helpertest.GenerationHarness',
                            [build/name, side, neoforge, overlay, mode], classpath=classpath,
                            jvm_args=jvm_args, expected_error=expected_error)
        if expected_error is None:
            path = build/name/'result.json'; detail = strict_bytes(path.read_bytes())
            if detail.get('pass') is not True:
                raise ValueError('Generation harness report failed: ' + name)
            if mode in ('normal', 'all-configs') and len(detail['actual_native_consumer_cases']) != 15:
                raise ValueError('Generation native consumer case count differs')
            generation_details[name] = dict(report_sha256=sha(path.read_bytes()), **detail)
    generation_case('generation-client', side='CLIENT')
    generation_case('generation-server')
    generation_case('generation-missing-site', mode='missing-site',
                    expected_error='Generation error consumer shape changed before transformation')
    for target in ['GenerationBar', 'CommandUtils']:
        member = next(n for n in repair['classes'] if n.endswith('/'+target+'.class'))
        generation_case('generation-missing-'+target.lower(), mode='guard-disabled',
                        jvm_args=['-Datm11.helper.hideResourcePrefix='+member])
        with zipfile.ZipFile(neoforge) as archive:
            raw = archive.read(member)
        old = (target+'.java').encode()
        if raw.count(old) != 1:
            raise ValueError('Unexpected GenerationBar SourceFile fixture')
        changed = raw.replace(old, b'X'+old[1:])
        fixture_jar = build/('changed-'+target.lower()+'.jar')
        with zipfile.ZipFile(fixture_jar, 'w') as archive:
            archive.writestr(member, changed)
        generation_case('generation-changed-'+target.lower(), mode='guard-disabled', prefix=[fixture_jar])
    generation_case('generation-server-no-client-mods', mode='all-configs')
    checked_package()
    for path, digest in inputs.items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Verification input changed: ' + path)
    for relative, expected in report['source_files'].items():
        if sha((HERE / relative).read_bytes()) != expected:
            raise ValueError('Source changed during verification: ' + relative)
    inputs_after = {path: sha(Path(path).read_bytes()) for path in inputs}
    if inputs_after != inputs:
        raise ValueError('Verification input changed during verification')
    input_labels = {str(jar): '<HELPER_JAR>', str(quarry): '<QUARRY_JAR>',
                    str(mining): '<MINING_JAR>', str(measurements): '<MEASUREMENTS_JAR>', str(overlay): '<LANGUAGE_PACK>'}
    for library in libraries:
        input_labels[str(library)] = '<PRISM_LIBRARY>/' + library.name
    before_sanitized = {input_labels[path]: digest for path, digest in inputs.items()}
    after_sanitized = {input_labels[path]: digest for path, digest in inputs_after.items()}
    summary = {'schema_version': 4, 'pass': True, 'status': 'completed', 'helper_sha256': sha(jar.read_bytes()), 'results': results,
               'generation_repair_runtime_contract': generation_runtime,
               'generation_details': generation_details,
               'generation_native_consumer_cases': sum(len(d.get('actual_native_consumer_cases', [])) for d in generation_details.values()),
               'generation_language_pack_sha256': sha(overlay.read_bytes()),
               'independently_reviewed_helper_labels': 46, 'quarry_label_injection_sites': 12,
               'mining_precision_injection_sites': 2, 'measurements_enum_labels': 35,
               'optional_feature_isolation_modes': list(modes),
               'measurements_guard_modes': list(measurements_modes),
               'case_count': len(results),
               'input_files_unchanged': True,
               'input_hashes_before': before_sanitized, 'input_hashes_after': after_sanitized,

               'quarry_jar_sha256': sha(quarry.read_bytes()), 'mining_jar_sha256': sha(mining.read_bytes()),
               'measurements_jar_sha256': sha(measurements.read_bytes()),
               'measurements_runtime_guards': measurements_runtime,
               'measurements_asset_checks': language_observation,
               'no_game_launch': True,
               'no_installation': True, 'visual_qa': False}
    (build / 'verification-report.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    out = HERE/'build/verification-report.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({'pass':False,'status':'started'})+'\n')
    try:
        main()
    except BaseException as error:
        out.write_text(json.dumps({'pass':False,'status':'failed','error':str(error)})+'\n')
        raise
