#!/usr/bin/env python3
"""Serial, fresh-process A/A and A/B benchmark with independent quality checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import re
import signal
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from generate import generate, sha
from quality import parse_quast, quality_gate

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def measured(cmd, folder, timeout):
    folder.mkdir(parents=True, exist_ok=False)
    write_json(folder/'command.json', cmd)
    start = time.monotonic()
    with (folder/'stdout.log').open('w') as out, (folder/'stderr.log').open('w') as err:
        proc = subprocess.Popen(cmd, stdout=out, stderr=err, start_new_session=True,
                                env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1'))
        while True:
            pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
            if pid:
                proc.returncode = os.waitstatus_to_exitcode(status)
                break
            if time.monotonic() - start > timeout:
                os.killpg(proc.pid, signal.SIGKILL)
                os.wait4(proc.pid, 0)
                proc.returncode = -9
                raise RuntimeError('Timed out: ' + str(folder))
            time.sleep(.01)
    result = {'wall_seconds': time.monotonic() - start,
              'user_seconds': usage.ru_utime, 'system_seconds': usage.ru_stime,
              'peak_rss_bytes': usage.ru_maxrss * (1 if platform.system() == 'Darwin' else 1024),
              'exit_code': proc.returncode}
    write_json(folder/'resources.json', result)
    if proc.returncode != 0:
        raise RuntimeError('Nonzero exit; see ' + str(folder/'stderr.log'))
    return result


def quast(assemblies, reference, out):
    cmd = [sys.executable, str(ROOT/'vendor/quast/quast.py'), *map(str, assemblies),
           '-r', str(reference), '-o', str(out), '-t', '1', '-m', '500',
           '--no-plots', '--no-html', '--no-icarus', '--no-sv', '--no-read-stats', '--strict-NA']
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.with_suffix('.log').open('w') as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
    write_json(out/'command.json', cmd)
    return parse_quast(out/'report.tsv')


def assemble(ds, window, folder, config):
    prefix = (folder/'asm').resolve()
    cmd = [str(ROOT/'vendor/hifiasm/hifiasm'), *config['common_args'], '-w', str(window),
           '-o', str(prefix), str((ROOT/'data'/ds['id']/'reads.fa').resolve())]
    result = measured(cmd, folder, config['timeout_seconds'])
    gfas = list(folder.glob('asm*.p_ctg.gfa'))
    if len(gfas) != 1:
        raise RuntimeError('Expected exactly one primary GFA: ' + str(gfas))
    fasta = folder/'assembly.fa'
    n = 0
    with fasta.open('w') as out:
        for line in gfas[0].read_text().splitlines():
            fields = line.split('\t')
            if fields[0] == 'S':
                if fields[2] == '*': raise ValueError('Missing GFA sequence')
                out.write('>' + fields[1] + '\n' + fields[2] + '\n')
                n += 1
    if not n: raise ValueError('Empty primary assembly')
    text = (folder/'stderr.log').read_text()
    result.update(window=window, hashes={'primary_gfa': sha(gfas[0]), 'primary_fasta': sha(fasta)},
                  all_gfa_hashes={p.name: sha(p) for p in sorted(folder.glob('*.gfa'))},
                  # Raw timestamps are cumulative since start, never sum them as phase durations.
                  phase_markers=re.findall(r'\[M::([^\]]+)\][^\n]*', text),
                  seed_index_counts=[int(x) for x in re.findall(r'indexed (\d+) positions', text)],
                  folder=str(folder.relative_to(ROOT)))
    # Quality every observed output; no assumption that repetitions match.
    quality = quast([fasta.resolve()], (ROOT/'data'/ds['id']/'reference.fa').resolve(), folder/'quast')
    result['quality'] = next(iter(quality.values()))
    # Intermediates are not reused, and removing them bounds the disk footprint.
    for p in folder.glob('*.bin'): p.unlink()
    return result


def control(out, config):
    ds = config['datasets'][0]
    generate(ds, ROOT/'data'/ds['id'])
    ref = ROOT/'data'/ds['id']/'reference.fa'
    seq = ''.join(ref.read_text().splitlines()[1:])
    from generate import fasta, rc
    out.mkdir(parents=True, exist_ok=False)
    fasta(out/'truth.fa', 'truth', seq)
    # Internal inversion, two junctions; preserves length and N50.
    fasta(out/'wrong_inversion.fa', 'wrong', seq[:60000] + rc(seq[60000:120000]) + seq[120000:])
    metrics = quast([(out/'truth.fa').resolve(), (out/'wrong_inversion.fa').resolve()], ref, out/'quast')
    good, bad = metrics['truth'], metrics['wrong_inversion']
    assert good['misassemblies'] == 0 and good['genome_fraction'] == 100, good
    assert bad['misassemblies'] > 0, bad
    assert quality_gate(good, bad), 'Wrong assembly escaped quality gate'
    write_json(out/'control.json', {'positive': good, 'negative': bad, 'negative_rejected': True})
    print('PASS: QUAST truth control; rejected length-preserving inversion', flush=True)


def bootstrap_ci(values):
    rng = random.Random(811)
    means = sorted(statistics.median([values[int(rng.random()*len(values))] for _ in values]) for _ in range(4000))
    return [means[100], means[3900]]


def summarize(records, config):
    summaries = []
    for ds in config['datasets']:
        runs = [r for r in records if r['dataset'] == ds['id']]
        if not runs: continue
        aa, ab = [], []
        for phase, dest in [('aa', aa), ('ab', ab)]:
            for pair in sorted({r['pair'] for r in runs if r['phase'] == phase}):
                group = {r['arm']: r for r in runs if r['phase'] == phase and r['pair'] == pair}
                a, b = group['A'], group['B']
                dest.append({'speedup': a['wall_seconds']/b['wall_seconds'],
                             'cpu_speedup': (a['user_seconds'] + a['system_seconds']) / (b['user_seconds'] + b['system_seconds']),
                             'rss_ratio': b['peak_rss_bytes']/a['peak_rss_bytes'],
                             'exact_primary': a['hashes'] == b['hashes'],
                             'exact_all_gfa': a['all_gfa_hashes'] == b['all_gfa_hashes'],
                             'quality_failures': quality_gate(a['quality'], b['quality'])})
        speed = statistics.median(p['speedup'] for p in ab)
        noise = max(abs(p['speedup']-1) for p in aa)
        stable = all(p['exact_primary'] and p['exact_all_gfa'] and not p['quality_failures'] for p in aa)
        quality_ok = all(not p['quality_failures'] for p in ab)
        memory_ok = statistics.median(p['rss_ratio'] for p in ab) <= config['gates']['max_rss_ratio']
        ci = bootstrap_ci([p['speedup'] for p in ab])
        performance_ok = speed >= config['gates']['minimum_speedup'] and speed - 1 > 2*noise and ci[0] > 1
        row = {'dataset': ds['id'], 'split': ds['split'], 'aa_pairs': aa, 'ab_pairs': ab,
               'median_speedup': speed, 'paired_bootstrap_95pct': ci,
               'median_cpu_speedup': statistics.median(p['cpu_speedup'] for p in ab),
               'max_aa_relative_deviation': noise, 'aa_stable': stable,
               'quality_pass': quality_ok, 'memory_pass': memory_ok, 'performance_pass': performance_ok,
               'candidate_accepted': stable and quality_ok and memory_ok and performance_ok,
               'exact_primary_all_pairs': all(p['exact_primary'] for p in ab),
               'exact_all_gfa_all_pairs': all(p['exact_all_gfa'] for p in ab)}
        for arm in ['A', 'B']:
            data = [r for r in runs if r['phase'] == 'ab' and r['arm'] == arm]
            row[arm] = {'median_wall_seconds': statistics.median(r['wall_seconds'] for r in data),
                        'median_cpu_seconds': statistics.median(r['user_seconds'] + r['system_seconds'] for r in data),
                        'median_peak_rss_bytes': statistics.median(r['peak_rss_bytes'] for r in data),
                        'quality': data[0]['quality'], 'seed_index_counts': data[0]['seed_index_counts']}
        summaries.append(row)
    return summaries


def report(out, summaries):
    lines = ['# Controlled minimizer-window experiment', '',
             'LOCAL-ONLY, author checked. Window 51 → 101, same binary and inputs. See environment.json and commands for build/runtime provenance.', '',
             '| Dataset | Split | A seconds | B seconds | Wall speedup | CPU speedup | RSS A/B MiB | Quality | Exact primary GFA/FASTA | Screening gate |',
             '|---|---|---:|---:|---:|---:|---:|---|---|---|']
    for s in summaries:
        a, b = s['A'], s['B']
        lines.append(f"| {s['dataset']} | {s['split']} | {a['median_wall_seconds']:.3f} | {b['median_wall_seconds']:.3f} | {s['median_speedup']:.3f}× | {s['median_cpu_speedup']:.3f}× | {a['median_peak_rss_bytes']/2**20:.1f}/{b['median_peak_rss_bytes']/2**20:.1f} | {s['quality_pass']} | {s['exact_primary_all_pairs']} | {s['candidate_accepted']} |")
    lines += ['', '## Quality (first A/B pair; every repetition is checked)', '',
              '| Dataset/arm | Extensive/local errors | Genome % | Duplication | N50 | NG50 | NGA50 | Contigs | Mismatch/indel per 100kb |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for s in summaries:
        for arm in ['A', 'B']:
            q = s[arm]['quality']
            lines.append(f"| {s['dataset']}/{arm} | {q['misassemblies']:.0f}/{q['local_misassemblies']:.0f} | {q['genome_fraction']:.3f} | {q['duplication_ratio']:.3f} | {q['n50']:.0f} | {q['ng50']:.0f} | {q['nga50']:.0f} | {q['contigs']:.0f} | {q['mismatches_per_100kb']}/{q['indels_per_100kb']} |")
    lines += ['', '## Interpretation limits', '',
              'A/A output equality is required. Acceptance additionally requires all quality gates, ≥10% median speedup, gain exceeding twice the maximum A/A deviation, bootstrap lower bound >1, and median peak RSS ratio ≤1.05. Five pairs give only coarse uncertainty estimates; this is a pilot, not a significance claim.', '',
              'Timing is whole-process assembly time, including input and output; QUAST is outside the timed region. RSS is the OS per-process high-water mark including Rosetta where applicable. File caches are warm; assembly intermediate caches are never reused. One warmup per arm is excluded. No concurrent builds or pilot benchmarks run. External machine activity is recorded as load averages but not controlled. CPU ratios are additional diagnostics, not substitutes for an idle-machine replay. See reports/trial/HOST-CAVEAT.md for the initialization host: substantial competing activity was observed. Screening acceptance does not constitute a confirmed performance claim.', '',
              'The candidate changes seed selection and is a quality-risking parameter optimization. Byte equality on a finite set does not prove universal equivalence. All GFA equality is tracked separately from primary FASTA/GFA equality; binary intermediate identity is not claimed. No real biological, diploid or human generalization is established.', '',
              'Completeness means reference base coverage here, not gene/BUSCO completeness. Synthetic reads include simplistic substitutions and indels. Held-out sets were frozen before candidate evaluation; after this report they are regression datasets, requiring new holdouts for subsequent tuning.']
    (out/'REPORT.md').write_text('\n'.join(lines) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='reports/experiment')
    p.add_argument('--control-only', action='store_true')
    p.add_argument('--datasets', nargs='+', help='Subset; exploratory only unless all frozen datasets run')
    args = p.parse_args()
    config = json.loads(Path('configs/experiment.json').read_text())
    out = Path(args.out).resolve()
    if not out.is_relative_to(ROOT): raise ValueError('Output must remain inside the pilot')
    if args.control_only:
        control(out, config)
        return
    out.mkdir(parents=True, exist_ok=False)
    if args.datasets: config['datasets'] = [d for d in config['datasets'] if d['id'] in args.datasets]
    environment = {'time_utc': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
                   'python': sys.version, 'load_start': os.getloadavg(),
                   'config_sha256': sha(ROOT/'configs/experiment.json'),
                   'generator_sha256': sha(ROOT/'scripts/generate.py'),
                   'harness_sha256': sha(ROOT/'scripts/benchmark.py'),
                   'quality_sha256': sha(ROOT/'scripts/quality.py'),
                   'build': json.loads(Path('reports/setup/build.json').read_text()), 'configuration': config}
    write_json(out/'environment.json', environment)
    control(out/'verifier-control', config)
    records = []
    # Candidate and holdout definitions were frozen in config before any assembly run.
    for ds in config['datasets']:
        metadata = generate(ds, ROOT/'data'/ds['id'])
        write_json(out/(ds['id'] + '-inputs.json'), metadata)
        print('Dataset ' + ds['id'], flush=True)
        windows = config['frozen_candidate']
        for arm, window in [('A', windows['baseline_window']), ('B', windows['candidate_window'])]:
            assemble(ds, window, out/'runs'/(ds['id'] + '-warmup-' + arm), config)
        for phase, pairs in [('aa', config['aa_pairs']), ('ab', config['ab_pairs'])]:
            # Balanced AB/BA alternation, with first order fixed by recorded seed.
            reverse = random.Random(config['schedule_seed'] + ds['seed']).random() < .5
            for pair in range(pairs):
                order = ['B', 'A'] if (pair % 2 == int(reverse)) else ['A', 'B']
                for arm in order:
                    window = windows['candidate_window'] if phase == 'ab' and arm == 'B' else windows['baseline_window']
                    name = f"{ds['id']}-{phase}-{pair}-{arm}"
                    print('  ' + name + ' window=' + str(window), flush=True)
                    result = assemble(ds, window, out/'runs'/name, config)
                    result.update(dataset=ds['id'], split=ds['split'], phase=phase, pair=pair, arm=arm, load=os.getloadavg())
                    records.append(result)
                    write_json(out/'runs.json', records)
        summaries = summarize(records, config)
        write_json(out/'summary.json', summaries)
        report(out, summaries)
    environment['load_end'] = os.getloadavg()
    write_json(out/'environment.json', environment)
    print((out/'REPORT.md').read_text(), flush=True)

if __name__ == '__main__':
    main()
