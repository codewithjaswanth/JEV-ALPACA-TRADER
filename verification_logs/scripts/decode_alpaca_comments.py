# decode_alpaca_comments.py
from pathlib import Path

raw = Path('src/trading/alpaca_manager.py').read_bytes()
lines = raw.splitlines(keepends=True)

out = []
for lnum in [440, 460, 464]:
    line_bytes = lines[lnum - 1]
    hex_str = line_bytes.hex()
    try:
        decoded = line_bytes.decode('gbk').strip()
    except Exception as e:
        decoded = f'Decode error: {e}'
    out.append(f'Line {lnum}:')
    out.append(f'  Hex: {hex_str}')
    out.append(f'  Decoded GBK (hypothesis): {decoded}\n')

res = '\n'.join(out)
Path('../verification_logs/stage1c/decoded_comments.log').write_text(res, encoding='utf-8')
print(res.encode('ascii', errors='backslashreplace').decode('ascii'))
