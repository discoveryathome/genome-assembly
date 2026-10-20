#!/usr/bin/env python3
"""Package completed evidence. Does not run an assembler or promote a candidate."""
import json
from pathlib import Path
import statistics
import hashlib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/experiment'

def put(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    environment = json.loads((OUT/'environment.json').read_text())
    config = environment['configuration']
    records = json.loads((OUT/'runs.json').read_text())
    summaries = json.loads((OUT/'summary.json').read_text())
    assert len(summaries) == len(config['datasets']) == 3, 'Experiment incomplete'
    assert len(records) == 3*2*(config['aa_pairs']+config['ab_pairs']) == 42
    baseline = {}
    table = []
    for summary in summaries:
        name = summary['dataset']
        a = [r for r in records if r['dataset']==name and r['arm']=='A' and r['phase']=='ab']
        baseline[name] = {'hashes':a[0]['hashes'], 'quality':a[0]['quality'],
                          'all_gfa_hashes':a[0]['all_gfa_hashes'],
                          'performance':summary['A'], 'build':environment['build']['binaries'],
                          'input_sha256':json.loads((OUT/(name+'-inputs.json')).read_text())['sha256']}
        assert all(x['hashes']==a[0]['hashes'] and x['quality']==a[0]['quality'] for x in a)
        acount = sum(summary['A']['seed_index_counts'])
        bcount = sum(summary['B']['seed_index_counts'])
        table.append({'case':name, 'split':summary['split'], 'cpu_speedup':summary['median_cpu_speedup'],
                      'wall_speedup':summary['median_speedup'],
                      'baseline_cpu_seconds':summary['A']['median_cpu_seconds'],
                      'candidate_cpu_seconds':summary['B']['median_cpu_seconds'],
                      'seed_occurrences_A':acount,'seed_occurrences_B':bcount,
                      'seed_reduction_pct':100*(1-bcount/acount),
                      'cpu_reduction_pct':100*(1-1/summary['median_cpu_speedup']),
                      'cpu_aa_max_relative_deviation':max(abs(x['cpu_speedup']-1) for x in summary['aa_pairs']),
                      'wall_aa_max_relative_deviation':summary['max_aa_relative_deviation'],
                      'quality_pass':summary['quality_pass'],
                      'all_gfa_byte_identical':summary['exact_all_gfa_all_pairs'],
                      'screening_pass':summary['candidate_accepted'],
                      'by':'Codex-assisted local trial', 'source':'reports/experiment/runs.json',
                      'updated':'2026-10-20'})
    put(OUT/'baseline.json',baseline)
    put(OUT/'case-table.json',table)
    put(OUT/'trial-totals.json',{
        'measured_assembly_runs':len(records), 'warmup_runs':6,
        'sum_measured_wall_seconds':sum(r['wall_seconds'] for r in records),
        'sum_measured_cpu_seconds':sum(r['user_seconds']+r['system_seconds'] for r in records),
        'peak_rss_range_MiB':[min(r['peak_rss_bytes'] for r in records)/2**20,max(r['peak_rss_bytes'] for r in records)/2**20],
        'cpu_seconds_range':[min(r['user_seconds']+r['system_seconds'] for r in records),max(r['user_seconds']+r['system_seconds'] for r in records)],
        'all_cases_quality_pass':all(s['quality_pass'] for s in summaries),
        'all_cases_exact_all_gfa':all(s['exact_all_gfa_all_pairs'] for s in summaries),
        'all_cases_screening_pass':all(s['candidate_accepted'] for s in summaries),
        'performance_promotion':'withheld: severe host contention, Rosetta, no independent replay',
        'scientific_generalization':'three synthetic miniature circular genomes only; published heldouts are now regression inputs'
    })
    package=ROOT/'packages/window101'; package.mkdir(parents=True,exist_ok=True)
    put(package/'TASK.json',{
        'task':'overlap-seeding-01','priority_revision':1,'scope_status':'refined',
        'reason':'Single size-only pivot from 250–400 kbp to a frozen 60–100 kbp starter tier after sizing under severe host contention; candidate/gates/repetitions unchanged.',
        'outcome':'completed parameter experiment; performance promotion withheld',
        'evidence_level':'local-only','algorithm_novelty':'none claimed: existing minimizer-window parameter',
        'next_questions':[
            {'question':'Does the CPU improvement survive an idle native-x86 replay?','why_it_matters':'Host contention and Rosetta prevent a portable speed claim.','first_step':['python3','scripts/benchmark.py','--out','reports/replay-001'],'blocked_by':'An idle host and compatible QUAST Python'},
            {'question':'Can a short session improve a measured seed/chaining kernel while preserving all anchors?','why_it_matters':'Parameter tuning does not demonstrate repeatable algorithmic progress.','first_step':['python3','scripts/first_step.py','overlap-seeding'],'blocked_by':'A native profile and a differential kernel test corpus'},
            {'question':'How should duplicated circular closure be scored for a real public microbial dataset?','why_it_matters':'Current synthetic baseline contains duplication and a reported relocation.','first_step':['python3','scripts/first_step.py','verifier'],'blocked_by':'Domain review; no reference-based repair during assembly'}
        ]})
    sources={str(p.relative_to(ROOT)):digest(p) for p in [ROOT/environment['config_path'], ROOT/'configs/tools.lock.json', OUT/'environment.json', OUT/'runs.json', OUT/'summary.json', OUT/'baseline.json', OUT/'case-table.json']}
    put(package/'SOURCES.json',{'pilot_base':'e79fd3f02f8f4e1b771bd13b3b9c7afc11a4bbc3','frozen_starter_commit':'73293e6','pins':environment['build']['pins'],'sha256':sources,'input_manifests':[str(p.relative_to(ROOT)) for p in sorted(OUT.glob('*-inputs.json'))]})
    put(package/'VERIFY.json',{'commands':[['python3','scripts/test_quality.py'],['python3','scripts/verify.py','reports/experiment'],['python3','tools/discover.pyz','validate','.']], 'full_replay':[['python3','scripts/bootstrap.py','--allow-unsandboxed'],['python3','scripts/benchmark.py','--out','reports/replay-001'],['python3','scripts/verify.py','reports/replay-001']], 'permission_note':'Unsandboxed flag requires owner permission; this session already has it. Use --sandboxed in an actual sandbox. No external posts.', 'assembly_timeout_seconds':180, 'quast_timeout_seconds':120, 'prerequisites':'Python 3.9+ for archived verifier; compiler/make/zlib and distutils-compatible Python for full replay. See README.'})
    # This hash inventory checks accidental evidence drift, not authenticity of a malicious author's claim.
    inventory={str(p.relative_to(OUT)):digest(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256.json'}
    put(OUT/'SHA256.json',inventory)
    print(json.dumps(table,indent=2)); print((OUT/'trial-totals.json').read_text())

if __name__=='__main__':main()
