# item4_notebook_audit.py
import sys
import json
import re
import ast
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

nb_path = Path("examples/FinRL_Full_selection.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}\n")

alpaca_keywords = ["alpaca", "apca", "paper-api", "tradingclient", "order", "trade_executor"]
neutralized_set = {1, 2, 8, 9, 10, 11, 12, 13, 14}
unneutralized_alpaca_refs = []

for idx, cell in enumerate(nb["cells"]):
    c_type = cell.get("cell_type")
    source = "".join(cell.get("source", []))
    lines = source.splitlines()
    first_line = lines[0].strip() if lines else "(empty)"
    
    imports = []
    if c_type == "code":
        try:
            clean_code = "\n".join([l for l in lines if not l.startswith("!") and not l.startswith("%")])
            tree = ast.parse(clean_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for n in node.names:
                        imports.append(f"{mod}.{n.name}")
        except Exception:
            for l in lines:
                if l.strip().startswith(("import ", "from ")):
                    imports.append(l.strip())

    kw_matches = []
    for kw in alpaca_keywords:
        if re.search(r"\b" + re.escape(kw), source, re.IGNORECASE):
            kw_matches.append(kw)
            
    if kw_matches and idx not in neutralized_set:
        unneutralized_alpaca_refs.append((idx, kw_matches, first_line))
        
    domains = []
    needs_key = []
    s_lower = source.lower()
    if "fmp" in s_lower or "financialmodelingprep" in s_lower:
        domains.append("financialmodelingprep.com")
        needs_key.append("FMP_API_KEY (paid/personal API key)")
    if "wrds" in s_lower:
        domains.append("wrds.wharton.upenn.edu")
        needs_key.append("WRDS credentials (Wharton research account)")
    if "yahoo" in s_lower or "yfinance" in s_lower or "sp500" in s_lower or "data_fetcher" in s_lower:
        domains.append("query1.finance.yahoo.com (public market data)")
        domains.append("en.wikipedia.org (public S&P500 table)")
    if "alpaca" in s_lower or "apca" in s_lower:
        domains.append("paper-api.alpaca.markets")
        needs_key.append("APCA_API_KEY / APCA_API_SECRET (Alpaca paper account)")

    print(f"Cell {idx:2d} [{c_type:8s}]: {first_line[:65]}")
    if imports:
        print(f"   Imports: {', '.join(imports)}")
    if kw_matches:
        print(f"   Alpaca/Order refs: {kw_matches}")
    if domains:
        print(f"   External contacts: {list(set(domains))}")
    if needs_key:
        print(f"   Key requirements: {list(set(needs_key))}")
    print("-" * 70)

print("\n=== CONFIRMATION OF CELLS OUTSIDE [1, 2, 8-14] ===")
if unneutralized_alpaca_refs:
    print(f"ALERT: Found {len(unneutralized_alpaca_refs)} unneutralized cells with references:")
    for idx, kw, fline in unneutralized_alpaca_refs:
        print(f"  Cell {idx}: matches {kw} - '{fline}'")
else:
    print("CONFIRMED: NO cell outside the neutralized set [1, 2, 8-14] references Alpaca, credentials, or orders.")
