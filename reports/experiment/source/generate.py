#!/usr/bin/env python3
"""Deterministic circular synthetic genomes. Not a calibrated HiFi simulator."""
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
COMPLEMENT = str.maketrans('ACGT', 'TGCA')

def rc(sequence):
    return sequence.translate(COMPLEMENT)[::-1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fasta(path, name, seq):
    path.write_text('>' + name + '\n' + '\n'.join(seq[i:i+80] for i in range(0, len(seq), 80)) + '\n')

def generate(spec, out):
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(spec['seed'])
    n, gc = spec['length'], spec['gc']
    # random() is specified stable across Python versions for a fixed seed.
    def base():
        x = rng.random()
        if x < gc / 2: return 'G'
        if x < gc: return 'C'
        if x < gc + (1-gc)/2: return 'A'
        return 'T'
    ref = ''.join(base() for _ in range(n))
    r = spec['repeat_length']
    source, dest = n//5, 3*n//5
    ref = ref[:dest] + ref[source:source+r] + ref[dest+r:]
    fasta(out/'reference.fa', 'synthetic_circle', ref)
    count = round(n * spec['coverage'] / ((spec['read_min'] + spec['read_max']) / 2))
    bases = 0
    with (out/'reads.fa').open('w') as f:
        for i in range(count):
            length = spec['read_min'] + int(rng.random() * (spec['read_max'] - spec['read_min'] + 1))
            start = int(rng.random() * n)
            seq = (ref + ref)[start:start+length]
            if rng.random() < .5: seq = rc(seq)
            mutated = []
            for b in seq:
                x = rng.random()
                if x < spec['indel_rate'] / 2:
                    continue
                if x < spec['indel_rate']:
                    mutated.append(base())
                if spec['indel_rate'] <= x < spec['indel_rate'] + spec['substitution_rate']:
                    other = ''.join(c for c in 'ACGT' if c != b)
                    b = other[int(rng.random() * 3)]
                mutated.append(b)
            read = ''.join(mutated)
            bases += len(read)
            f.write('>read_' + str(i) + '\n' + read + '\n')
    metadata = dict(spec, circular=True, read_count=count, read_bases=bases,
                    actual_coverage=bases/n, repeat_coordinates=[source, dest, r],
                    sha256={p.name: sha(p) for p in (out/'reference.fa', out/'reads.fa')})
    (out/'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return metadata

if __name__ == '__main__':
    spec = json.loads((ROOT/'configs/experiment.json').read_text())
    for ds in spec['datasets']:
        print(json.dumps(generate(ds, ROOT/'data'/ds['id'])))
