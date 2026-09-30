# execute_tutorial_copy.py
import json
import os
import sys
import traceback
from pathlib import Path

# Paths, all outside repo except reading source
repo_root = Path(os.getcwd()).resolve()
nb_src = repo_root / "examples" / "FinRL_Full_selection.ipynb"
log_dir = repo_root.parent / "verification_logs"
nb_copy_path = log_dir / "FinRL_Full_selection_copy.ipynb"
nb_out_path = log_dir / "FinRL_Full_selection_executed.ipynb"
log_path = log_dir / "tutorial_execution.log"

print("Reading source notebook: " + str(nb_src))
with open(nb_src, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Identify and neutralize cells
# Cells 8, 9, 10, 11, 12, 13, 14 touch Alpaca/orders/credentials
# Cells 1, 2 are IPython shell/magics (!pip install, %cd)
neutralized_cells = [1, 2, 8, 9, 10, 11, 12, 13, 14]

for idx in neutralized_cells:
    if idx < len(nb["cells"]):
        cell = nb["cells"][idx]
        if cell["cell_type"] == "code":
            cell["source"] = [
                "# Neutralized offline-safe: originally Cell " + str(idx) + " touched Alpaca/orders/credentials or shell magics\n",
                "pass\n"
            ]

# Save copy outside repo
with open(nb_copy_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
print("Saved neutralized copy to " + str(nb_copy_path))

# Execute cells non-interactively
exec_globals = {
    "__name__": "__main__",
    "__file__": str(nb_copy_path),
}
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

results = []
log_lines = []
log_lines.append("Starting non-interactive execution of " + str(nb_copy_path) + "\n")
first_failure = None

for idx, cell in enumerate(nb["cells"]):
    c_type = cell.get("cell_type")
    source = "".join(cell.get("source", []))
    header = source.splitlines()[0] if source.splitlines() else "(empty)"

    if idx in [8, 9, 10, 11, 12, 13, 14]:
        res = {"cell": idx, "type": c_type, "status": "SKIPPED", "reason": "Neutralized: touches Alpaca/credentials/orders"}
        results.append(res)
        log_lines.append("Cell " + str(idx) + " [" + str(c_type) + "]: SKIPPED (" + res["reason"] + ")\n")
        continue

    if idx in [1, 2]:
        res = {"cell": idx, "type": c_type, "status": "SKIPPED", "reason": "Neutralized: IPython magic (!pip / %cd)"}
        results.append(res)
        log_lines.append("Cell " + str(idx) + " [" + str(c_type) + "]: SKIPPED (" + res["reason"] + ")\n")
        continue

    if c_type == "markdown":
        res = {"cell": idx, "type": c_type, "status": "COMPLETED", "reason": "Markdown"}
        results.append(res)
        log_lines.append("Cell " + str(idx) + " [markdown]: COMPLETED\n")
        continue

    if c_type == "code":
        log_lines.append("Cell " + str(idx) + " [code]: Executing: " + header[:60] + "...\n")
        print("Executing Cell " + str(idx) + " [code]...")
        try:
            code_obj = compile(source, "<cell_" + str(idx) + ">", "exec")
            exec(code_obj, exec_globals)
            res = {"cell": idx, "type": c_type, "status": "COMPLETED", "reason": "Executed without error"}
            results.append(res)
            log_lines.append("Cell " + str(idx) + " [code]: COMPLETED (executed without error)\n")
        except Exception as e:
            tb = traceback.format_exc()
            res = {
                "cell": idx,
                "type": c_type,
                "status": "FAILED",
                "error": type(e).__name__ + ": " + str(e),
                "traceback": tb,
            }
            results.append(res)
            log_lines.append("Cell " + str(idx) + " [code]: FAILED (" + type(e).__name__ + ": " + str(e) + ")\n" + tb + "\n")
            first_failure = res
            print("Cell " + str(idx) + " FAILED: " + type(e).__name__ + ": " + str(e))
            break

with open(nb_out_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

with open(log_path, "w", encoding="utf-8") as f:
    f.writelines(log_lines)

print("\n=== EXECUTION SUMMARY ===")
for r in results:
    print("Cell " + str(r["cell"]) + " (" + str(r["type"]) + "): " + str(r["status"]) + " - " + str(r.get("reason", r.get("error", ""))))

if first_failure:
    print("\nExecution STOPPED at Cell " + str(first_failure["cell"]) + " due to failure.")
    sys.exit(1)
sys.exit(0)
