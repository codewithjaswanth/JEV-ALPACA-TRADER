# smoke_check.py
import sys
import os
import importlib

# Add current working directory (repo root) to sys.path
sys.path.insert(0, os.getcwd())

modules = [
    "src.config.settings",
    "src.data.data_fetcher",
    "src.data.data_processor",
    "src.data.data_store",
    "src.backtest.backtest_engine",
    "src.strategies.base_strategy",
    "src.strategies.ml_strategy",
    "src.trading.alpaca_manager",
    "src.trading.trade_executor",
    "src.trading.performance_analyzer",
    "src.main",
]

results = {}
for mod in modules:
    try:
        importlib.import_module(mod)
        results[mod] = "PASS"
        print(f"success: executed without error - {mod}")
    except Exception as e:
        results[mod] = fstr = f"raised error: {type(e).__name__}: {e}"
        print(f"raised error: {mod}: {type(e).__name__}: {e}")

failed = [m for m, res in results.items() if "raised error" in res]
if failed:
    sys.exit(1)
sys.exit(0)
