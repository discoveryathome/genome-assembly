#!/usr/bin/env python3
"""Fetch pinned sources, screen, and build locally. Never installs global packages."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

def run(args, **kw):
    return subprocess.run(args, check=True, text=True, **kw)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--allow-unsandboxed', action='store_true', help='Use only with owner permission, or run inside a sandbox')
    p.add_argument('--sandboxed', action='store_true')
    a = p.parse_args()
    if not (a.allow_unsandboxed or a.sandboxed):
        p.error('Confirm screened execution permission using --allow-unsandboxed, or run sandboxed with --sandboxed')
    if shutil.disk_usage(ROOT).free < 10 * 1024**3:
        raise SystemExit('Need at least 10 GiB free before build')
    candidates = [os.environ.get('QUAST_PYTHON'), sys.executable, '/usr/bin/python3']
    quast_python = None
    for interpreter in candidates:
        if interpreter and Path(interpreter).exists() and subprocess.run(
                [interpreter, '-c', 'from distutils.version import LooseVersion'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            quast_python = interpreter
            break
    if quast_python is None:
        raise SystemExit('Pinned QUAST requires distutils: set QUAST_PYTHON to a Python 3.9–3.11 interpreter, then rerun bootstrap.')
    locks = json.loads(Path('configs/tools.lock.json').read_text())
    for name in ('vendor', 'tools', 'reports/setup', 'research'):
        Path(name).mkdir(parents=True, exist_ok=True)
    helper = Path('tools/discover.pyz')
    if not helper.exists():
        urllib.request.urlretrieve(locks['discover']['url'], helper)
    assert hashlib.sha256(helper.read_bytes()).hexdigest() == locks['discover']['sha256']
    for name in ('hifiasm', 'quast'):
        target = Path('vendor') / name
        pin = locks[name]
        if not target.exists():
            run(['git', 'init', str(target)], stdout=subprocess.DEVNULL)
            run(['git', '-C', str(target), 'remote', 'add', 'origin', pin['url']])
            run(['git', '-C', str(target), 'fetch', '--depth', '1', 'origin', pin['commit']])
            run(['git', '-C', str(target), 'checkout', '--detach', 'FETCH_HEAD'])
        head = subprocess.check_output(['git', '-C', str(target), 'rev-parse', 'HEAD'], text=True).strip()
        assert head == pin['commit'], (name, 'Wrong source revision')
        # Only our documented removal of a committed native extension is allowed.
        dirty = subprocess.check_output(['git', '-C', str(target), 'diff', '--name-only'], text=True).splitlines()
        assert set(dirty) <= ({'quast_libs/site_packages/simplejson/_speedups.so'} if name == 'quast' else set()), dirty
        scan = subprocess.run([sys.executable, str(helper), 'screen', str(target)], text=True, capture_output=True)
        Path('reports/setup/' + name + '-screen.txt').write_text(scan.stdout + scan.stderr)
        if '[high]' in scan.stdout.lower() or '[high]' in scan.stderr.lower() or scan.returncode not in (0, 1):
            raise SystemExit('Source screen requires review: ' + name)
    # Do not allow importing the repository's committed Mach-O extension.
    Path('vendor/quast/quast_libs/site_packages/simplejson/_speedups.so').unlink(missing_ok=True)
    flags = '-g -O3 -msse4.2 -mpopcnt -fomit-frame-pointer -Wall'
    translated = platform.system() == 'Darwin' and platform.machine() == 'arm64'
    if translated:
        run(['/usr/bin/arch', '-x86_64', '/usr/bin/true'])
        flags += ' -arch x86_64'
    elif platform.machine() not in ('x86_64', 'AMD64'):
        raise SystemExit('Hifiasm native ARM build is not part of this pilot')
    commands = [
        ['make', '-C', 'vendor/hifiasm', '-j2', 'CXX=c++', 'CC=cc', 'CXXFLAGS=' + flags],
        ['make', '-C', 'vendor/quast/quast_libs/minimap2', '-j2'] + (['aarch64=1'] if platform.machine() == 'arm64' else [])
    ]
    started = time.time()
    for i, cmd in enumerate(commands):
        with Path('reports/setup/build-' + str(i) + '.log').open('w') as log:
            run(cmd, stdout=log, stderr=subprocess.STDOUT)
    binaries = ['vendor/hifiasm/hifiasm', 'vendor/quast/quast_libs/minimap2/minimap2']
    provenance = {
        'platform': platform.platform(), 'machine': platform.machine(), 'python': sys.version,
        'translated_hifiasm': translated, 'commands': commands, 'pins': locks,
        'quast_python': quast_python,
        'quast_python_version': subprocess.check_output([quast_python, '--version'], text=True).strip(),
        'compiler': subprocess.check_output(['c++', '--version'], text=True),
        'build_seconds': time.time() - started,
        'binaries': {s: hashlib.sha256(Path(s).read_bytes()).hexdigest() for s in binaries},
        'versions': {s: subprocess.check_output([s, '--version'], text=True).strip() for s in binaries}
    }
    Path('reports/setup/build.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps(provenance, indent=2))

if __name__ == '__main__':
    main()
