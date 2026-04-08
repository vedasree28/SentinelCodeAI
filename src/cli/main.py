import argparse
import os

from src.core.secrets import detect_secrets
from src.core.leaks import detect_leaks
from src.ai.fixer import suggest_fix
from src.ai.nlp import detect_nlp
from src.ai.rules import FIX_RULES

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


# 🎨 Severity color mapping
def get_color(severity):
    return {
        "CRITICAL": "bold red",
        "HIGH": "red",
        "MEDIUM": "yellow",
        "LOW": "green"
    }.get(severity, "white")


# 🔍 Scan single file
def scan_file(file_path):
    console.print(f"\n[bold cyan]🔍 Scanning:[/bold cyan] {file_path}")

    safe_path = os.path.realpath(file_path)
    if not os.path.isfile(safe_path):
        return []
    try:
        with open(safe_path, "r", encoding="utf-8", errors="ignore") as f:  # nosec
            code = f.read()
    except OSError:
        return []

    secrets = detect_secrets(code)
    leaks = detect_leaks(file_path)
    issues = [*secrets, *[{"type": "Unclosed File", "value": leak} for leak in leaks]]

    # 🧠 NLP findings (optional context only)
    nlp_findings = detect_nlp(code)

    return issues, nlp_findings


# 🎯 Display issues
def display_results(all_issues, all_nlp):
    if not all_issues and not all_nlp:
        console.print("[bold green]✅ No issues found[/bold green]")
        return

    # 🔥 Sort by priority
    all_issues.sort(key=lambda x: FIX_RULES.get(x["type"], {}).get("priority", 3))

    severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

    # 🔐 Display Issues
    for issue in all_issues:
        fix_output = suggest_fix(issue)
        rule = FIX_RULES.get(issue["type"], {})
        severity = rule.get("severity", "LOW")

        severity_count[severity] += 1

        console.print(Panel(
            fix_output,
            title=f"[{get_color(severity)}]{issue['type']}[/{get_color(severity)}]",
            border_style=get_color(severity),
            box=box.ROUNDED
        ))

    # 🧠 NLP Findings (context only)
    if all_nlp:
        console.print("\n[bold magenta]🧠 Context Insights:[/bold magenta]")
        for n in all_nlp:
            console.print(
                f"[magenta]- [{n['risk']}] '{n['keyword']}' at line {n['line']} → {n['value']}[/magenta]"
            )

    # 📊 Summary Table
    table = Table(title="📊 Scan Summary", box=box.SIMPLE)

    table.add_column("Severity", justify="center")
    table.add_column("Count", justify="center")

    for sev, count in severity_count.items():
        if count > 0:
            table.add_row(sev, str(count))

    console.print("\n")
    console.print(table)

    # 🚫 Final Decision
    if severity_count["CRITICAL"] or severity_count["HIGH"]:
        console.print("\n🚫 [bold red]Commit Blocked due to critical issues[/bold red]")
    else:
        console.print("\n✅ [bold green]Safe to proceed[/bold green]")


# 📁 Scan path
def scan_path(path):
    path = os.path.abspath(path)

    all_issues = []
    all_nlp = []

    if os.path.isfile(path):
        issues, nlp = scan_file(path)
        all_issues.extend(issues)
        all_nlp.extend(nlp)
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    issues, nlp = scan_file(full_path)
                    all_issues.extend(issues)
                    all_nlp.extend(nlp)

    display_results(all_issues, all_nlp)


# 🚀 Entry point
def main():
    parser = argparse.ArgumentParser(description="SentinelCode AI")
    parser.add_argument("--path", required=True, help="File or folder to scan")

    args = parser.parse_args()

    scan_path(args.path)


if __name__ == "__main__":
    main()