# item3_requirements_audit.py
import re
from pathlib import Path

req_path = Path("requirements.txt")
lines = req_path.read_text(encoding="utf-8").splitlines()

packages = []
for idx, line in enumerate(lines, start=1):
    line_clean = line.strip()
    if not line_clean or line_clean.startswith("#"):
        continue
    spec = line_clean.split("#")[0].strip()
    packages.append((idx, spec))

stdlib_backports = ["pathlib"]
unbounded_lines = []
exact_pinned_lines = []
duplicate_checks = {}

for lnum, pkg_spec in packages:
    m = re.match(r"^([a-zA-Z0-9_\-\.]+)(.*)$", pkg_spec)
    if m:
        name, version_spec = m.group(1).lower(), m.group(2).strip()
        if name not in duplicate_checks:
            duplicate_checks[name] = []
        duplicate_checks[name].append((lnum, pkg_spec))
        
        if "<" not in version_spec and "==" not in version_spec:
            unbounded_lines.append((lnum, pkg_spec))
        if "==" in version_spec:
            exact_pinned_lines.append((lnum, pkg_spec))

print(f"Total non-comment requirement lines: {len(packages)}")
print(f"Total unpinned / lacking upper bound lines: {len(unbounded_lines)}")
print(f"Total exact-pinned (==) lines: {len(exact_pinned_lines)}")

print("\n=== OBSOLETE STDLIB BACKPORTS ===")
for lnum, pkg_spec in packages:
    name = re.match(r"^([a-zA-Z0-9_\-\.]+)", pkg_spec).group(1).lower()
    if name in stdlib_backports:
        print(f"Line {lnum}: {pkg_spec} (Standard library module in Python 3.4+; PyPI backport is obsolete)")

print("\n=== DUPLICATED PACKAGES ===")
duplicates = {k: v for k, v in duplicate_checks.items() if len(v) > 1}
if duplicates:
    for k, v in duplicates.items():
        print(f"Package '{k}' duplicated at: {v}")
else:
    print("No duplicated package lines found.")

print("\n=== UNBOUNDED / MINIMUM-ONLY PINNED LINES (NO UPPER BOUND) ===")
for lnum, pkg_spec in unbounded_lines:
    print(f"Line {lnum:2d}: {pkg_spec}")
