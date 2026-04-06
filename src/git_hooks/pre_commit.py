import sys
import subprocess
from src.core.secrets import detect_secrets
from src.core.leaks import detect_leaks
from src.core.severity import get_severity
from src.ai.fixer import suggest_fix

def get_staged_files():
    result = subprocess.check_output(
        ['git', 'diff', '--name-only', '--cached']
    )
    return result.decode().splitlines()

def run():
    files = get_staged_files()

    has_issues = False

    for file in files:
        try:
            with open(file, "r") as f:
                code = f.read()
        except:
            continue

        # 🔐 Secrets
        secrets = detect_secrets(code)
        for sec in secrets:
            severity = get_severity(sec["type"])
            print(f"[{severity}] Secret in {file}: {sec['value']}")
            print(suggest_fix(sec))
            has_issues = True

        # 🧠 Leaks
        leaks = detect_leaks(file)
        for leak in leaks:
            severity = "LOW"
            print(f"[{severity}] Leak in {file}: {leak}")
            print("🔧 Fix: Use proper resource handling")
            has_issues = True

    if has_issues:
        print("\n❌ Commit blocked due to issues.")
        sys.exit(1)

    print("✅ No issues found. Commit allowed.")

if __name__ == "__main__":
    run()