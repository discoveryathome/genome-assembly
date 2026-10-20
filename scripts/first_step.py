#!/usr/bin/env python3
"""Cheap task-card entry checks; no external execution or downloads."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('track', choices=['reproduce', 'verifier', 'overlap-seeding', 'literature'])
a = p.parse_args()
if a.track == 'reproduce':
    subprocess.run([sys.executable, str(ROOT/'scripts/verify.py'), 'reports/experiment'], check=True)
elif a.track == 'verifier':
    subprocess.run([sys.executable, str(ROOT/'scripts/test_quality.py')], check=True)
elif a.track == 'overlap-seeding':
    c = json.loads((ROOT/'configs/starter.json').read_text())
    print(json.dumps({'candidate': c['frozen_candidate'], 'common_args': c['common_args'], 'gates': c['gates']}, indent=2))
    print('Read reports/trial/NEXT-SESSION.md, then inspect pinned htab.cpp ha_pt_gen and anchor.cpp after bootstrap. No tuning on published holdouts.')
else:
    text = (ROOT/'research/BRIEF.md').read_text()
    assert '10.1038/s41592-020-01056-5' in text and '10.1093/bioinformatics/btt086' in text
    print(text)
