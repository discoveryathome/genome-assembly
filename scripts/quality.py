"""Fail-closed QUAST parser and quality/exactness gates; stdlib only."""
import math

FIELDS = {
    'misassemblies': '# misassemblies',
    'local_misassemblies': '# local misassemblies',
    'genome_fraction': 'Genome fraction (%)',
    'duplication_ratio': 'Duplication ratio',
    'n50': 'N50', 'ng50': 'NG50', 'nga50': 'NGA50',
    'contigs': '# contigs', 'total_length': 'Total length',
    'mismatches_per_100kb': '# mismatches per 100 kbp',
    'indels_per_100kb': '# indels per 100 kbp',
    'unaligned_length': 'Unaligned length'
}


def parse_quast(path):
    rows = [line.rstrip('\n').split('\t') for line in path.read_text().splitlines()]
    labels = rows[0][1:]
    raw = {r[0]: r[1:] for r in rows[1:]}
    result = {}
    for i, label in enumerate(labels):
        metrics = {}
        for key, field in FIELDS.items():
            if field not in raw or i >= len(raw[field]):
                raise ValueError('Missing QUAST field: ' + field)
            value = float(raw[field][i])  # '-' must FAIL, never become zero
            if not math.isfinite(value) or value < 0:
                raise ValueError('Invalid QUAST metric: ' + field)
            metrics[key] = value
        result[label] = metrics
    if not result:
        raise ValueError('Empty QUAST report')
    return result


def quality_gate(baseline, candidate):
    failures = []
    for key in FIELDS:
        for data in (baseline, candidate):
            if key not in data or not math.isfinite(data[key]) or data[key] < 0:
                raise ValueError('Missing or invalid metric: ' + key)
    for key in ('misassemblies', 'local_misassemblies', 'mismatches_per_100kb',
                'indels_per_100kb', 'unaligned_length', 'contigs'):
        if candidate[key] > baseline[key]:
            failures.append(key + ' increased')
    for key in ('genome_fraction', 'n50', 'ng50', 'nga50'):
        if candidate[key] < baseline[key]:
            failures.append(key + ' decreased')
    if abs(candidate['duplication_ratio'] - 1) > abs(baseline['duplication_ratio'] - 1) + 1e-12:
        failures.append('duplication error increased')
    return failures


def exact_gate(baseline_hashes, candidate_hashes):
    # The caller separately checks byte hashes of primary GFA and extracted FASTA.
    return baseline_hashes == candidate_hashes
