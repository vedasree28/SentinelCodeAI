import sys
import os
import subprocess
import shutil

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Fix encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.core.secrets import detect_secrets  # noqa: E402
from src.core.leaks import detect_leaks  # noqa: E402
from src.core.severity import get_severity  # noqa: E402
from src.ai.fixer import suggest_fix  # noqa: E402
from src.ai.nlp import detect_nlp  # noqa: E402

def _read_file(path: str):
    with open(os.path.realpath(path), "r", encoding="utf-8", errors="ignore") as f:  # nosec
        return f.read()

def run():
    git_path = shutil.which("git")
    if not git_path:
        sys.stderr.write("Error: git not found on PATH.\n")
        sys.exit(1)
    files = subprocess.check_output(
        [git_path, 'diff', '--name-only', '--cached']
    ).decode().splitlines()

    has_issues = False

    for file in files:
        if not file.endswith(".py"):
            continue
        if not os.path.exists(file):
             continue
        try:
            code = _read_file(file)
        except OSError as e:
            sys.stderr.write(f"Warning: could not read {file}: {e}\n")
            continue

        secrets = detect_secrets(code)
        leaks = detect_leaks(file)
        nlp_findings = detect_nlp(code)

        for sec in secrets:
            severity = get_severity(sec["type"])
            print(f"\n[{severity}] {sec['type']} detected in {file}")
            print(f"Value: {sec['value']}")
            print(suggest_fix(sec))
            has_issues = True

        for nlp in nlp_findings:
            print(f"\n[{nlp['risk']}] NLP: '{nlp['keyword']}' at line {nlp['line']} in {file}")
            print(f"Value: {nlp['value']}")
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