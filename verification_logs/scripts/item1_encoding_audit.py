# item1_encoding_audit.py
import subprocess
import sys
from pathlib import Path

target_file = Path('src/trading/alpaca_manager.py')
raw_bytes = target_file.read_bytes()

has_bom = raw_bytes.startswith(b'\xef\xbb\xbf')
print(f'BOM present: {has_bom}')

raw_lines = raw_bytes.splitlines(keepends=True)
invalid_lines = []

for line_idx, line in enumerate(raw_lines, start=1):
    try:
        line.decode('utf-8')
    except UnicodeDecodeError as e:
        invalid_lines.append((line_idx, line, e))

print(f'Total lines: {len(raw_lines)}')
print(f'Invalid UTF-8 line count: {len(invalid_lines)}')
print(f'Invalid UTF-8 line numbers: {[x[0] for x in invalid_lines]}')

if invalid_lines:
    first_num, first_bytes, first_err = invalid_lines[0]
    print(f'\nFirst offending line (line {first_num}):')
    print(f'Hex: {first_bytes.hex()}')
    print(f'Raw repr: {first_bytes!r}')
    try:
        decoded_gbk = first_bytes.decode('gbk')
        print(f'Decoded as GBK (hypothesis): {decoded_gbk.strip()}')
    except Exception as e:
        print(f'GBK decode error: {e}')

print('\n=== SCANNING ALL TRACKED .PY FILES FOR INVALID UTF-8 ===')
res = subprocess.run(['git', 'ls-files', '*.py'], capture_output=True, text=True, check=True)
tracked_py = res.stdout.splitlines()

offenders = {}
for py_path_str in tracked_py:
    p = Path(py_path_str)
    if not p.is_file():
        continue
    content = p.read_bytes()
    lines = content.splitlines()
    bad = []
    for idx, l in enumerate(lines, start=1):
        try:
            l.decode('utf-8')
        except UnicodeDecodeError:
            bad.append(idx)
    if bad:
        offenders[py_path_str] = bad

if offenders:
    print(f'Found {len(offenders)} files with invalid UTF-8:')
    for fpath, lnums in offenders.items():
        print(f'  - {fpath}: lines {lnums}')
else:
    print('No other tracked .py files contain invalid UTF-8.')
