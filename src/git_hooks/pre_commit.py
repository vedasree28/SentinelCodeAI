import sys
import os
import subprocess
from io import TextIOWrapper

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Fix encoding
if isinstance(sys.stdout, TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

from src.core.secrets import detect_secrets  # noqa: E402
from src.core.leaks import detect_leaks  # noqa: E402
from src.core.severity import get_severity  # noqa: E402
from src.ai.fixer import suggest_fix  # noqa: E402

def run():
    files = subprocess.check_output(
        ['git', 'diff', '--name-only', '--cached']
    ).decode().splitlines()

    has_issues = False

    for file in files:
        if not file.endswith(".py"):
            continue
        if not os.path.exists(file):
             continue
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
        except Exception:
            continue

        secrets = detect_secrets(code)
        leaks = detect_leaks(file)

        for sec in secrets:
            severity = get_severity(sec["type"])
            print(f"\n[{severity}] {sec['type']} detected in {file}")
            print(f"Value: {sec['value']}")
            print(suggest_fix(sec))
            has_issues = True

        for leak in leaks:
            print(f"\n[LOW] Leak in {file}: {leak}")
            print("Fix: Use 'with open(...) as f:'")
            has_issues = True

    if has_issues:
        print("\nCommit blocked due to issues.")
        sys.exit(1)

    print("No issues found. Commit allowed.")

if __name__ == "__main__":
    run()