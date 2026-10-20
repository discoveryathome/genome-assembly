#!/usr/bin/env python3
"""Replay recorded quality gates and resource summaries; no external binaries."""
import argparse
import json
from pathlib import Path
import tempfile
from benchmark import summarize, report
from generate import generate, sha
from quality import parse_quast, quality_gate

ROOT = Path(__file__).resolve().parents[1]


def verify(out, regenerate=True):
    config = json.loads((ROOT/'configs/experiment.json').read_text())
    environment = json.loads((out/'environment.json').read_text())
    assert environment['config_sha256'] == sha(ROOT/'configs/experiment.json'), 'Experiment definition changed'
    assert environment['configuration'] == config, 'Partial or altered experiment'
    locks = json.loads((ROOT/'configs/tools.lock.json').read_text())
    assert environment['build']['pins'] == locks, 'Dependency pin mismatch'
    for key, filename in [('generator_sha256', 'generate.py'), ('harness_sha256', 'benchmark.py'), ('quality_sha256', 'quality.py')]:
        assert environment[key] == sha(out/'source'/filename), 'Archived source drift: ' + filename
    records = json.loads((out/'runs.json').read_text())
    expected_count = len(config['datasets']) * 2 * (config['aa_pairs'] + config['ab_pairs'])
    assert len(records) == expected_count, 'Missing or duplicate benchmark runs'
    seen = set()
    for run in records:
        key = (run['dataset'], run['phase'], run['pair'], run['arm'])
        assert key not in seen, 'Duplicate record'
        seen.add(key)
        folder = (ROOT/run['folder']).resolve()
        assert folder.is_relative_to(out.resolve()), 'Escaping evidence folder'
        resources = json.loads((folder/'resources.json').read_text())
        for metric, value in resources.items():
            assert run[metric] == value, 'Resource record drift'
        assert run['exit_code'] == 0 and run['wall_seconds'] > 0 and run['peak_rss_bytes'] > 0
        assert run['quality'] == next(iter(parse_quast(folder/'quast/report.tsv').values())), 'Quality record drift'
        assert run['hashes']['primary_fasta'] == sha(folder/'assembly.fa'), 'FASTA corruption'
        primary = list(folder.glob('asm*.p_ctg.gfa'))
        assert len(primary) == 1
        assert run['hashes']['primary_gfa'] == sha(primary[0]), 'GFA corruption'
        assert run['all_gfa_hashes'] == {p.name: sha(p) for p in sorted(folder.glob('*.gfa'))}
        cmd = json.loads((folder/'command.json').read_text())
        common = config['common_args']
        assert cmd[1:1+len(common)] == common
        expected_window = config['frozen_candidate']['candidate_window'] if run['phase'] == 'ab' and run['arm'] == 'B' else config['frozen_candidate']['baseline_window']
        assert cmd[1+len(common):3+len(common)] == ['-w', str(expected_window)]
        assert run['window'] == expected_window
    for ds in config['datasets']:
        for phase, n in [('aa', config['aa_pairs']), ('ab', config['ab_pairs'])]:
            for pair in range(n):
                for arm in ('A', 'B'):
                    assert (ds['id'], phase, pair, arm) in seen, 'Missing required case'
    controls = parse_quast(out/'verifier-control/quast/report.tsv')
    assert controls['truth']['misassemblies'] == 0 and controls['truth']['genome_fraction'] == 100
    assert controls['wrong_inversion']['misassemblies'] > 0
    assert quality_gate(controls['truth'], controls['wrong_inversion'])
    derived = summarize(records, config)
    assert derived == json.loads((out/'summary.json').read_text()), 'Derived verdict differs from summary'
    # Finite evidence can show rejected candidates as a VALID research outcome.
    assert all(s['aa_stable'] for s in derived), 'A/A instability invalidates comparison'
    if regenerate:
        (ROOT/'scratch').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'scratch') as tmp:
            for ds in config['datasets']:
                metadata = generate(ds, Path(tmp)/ds['id'])
                assert metadata == json.loads((out/(ds['id']+'-inputs.json')).read_text()), 'Input regeneration mismatch'
    baseline = out/'baseline.json'
    if baseline.exists():
        pins = json.loads(baseline.read_text())
        for ds in config['datasets']:
            runs = [r for r in records if r['dataset'] == ds['id'] and r['window'] == 51]
            assert all(r['hashes'] == pins[ds['id']]['hashes'] and r['quality'] == pins[ds['id']]['quality'] for r in runs)
    print('PASS: pinned inputs, raw artifacts, QUAST controls, A/A stability and derived verdicts')
    for s in derived:
        print(s['dataset'], 'quality=' + str(s['quality_pass']), 'speedup=' + format(s['median_speedup'], '.3f'), 'accepted=' + str(s['candidate_accepted']))
    return derived

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('report', nargs='?', default='reports/experiment')
    p.add_argument('--skip-regenerate', action='store_true')
    args = p.parse_args()
    try:
        verify((ROOT/args.report).resolve(), regenerate=not args.skip_regenerate)
    except (AssertionError, ValueError, KeyError, FileNotFoundError) as exc:
        raise SystemExit('FAIL: ' + str(exc))
