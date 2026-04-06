import argparse
import os
from src.core.secrets import detect_secrets
from src.core.leaks import detect_leaks
from src.ai.fixer import suggest_fix
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def scan_file(file_path):
    console.print(f"\n[bold cyan]🔍 Scanning:[/bold cyan] {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception:
        return

    secrets = detect_secrets(code)
    leaks = detect_leaks(file_path)

    if not secrets and not leaks:
        console.print("[bold green]✅ No issues found[/bold green]")
        return

    if secrets:
        console.print("\n[bold red]🔐 Secrets Found:[/bold red]")
        for s in secrets:
            console.print(Panel(
                f"[bold]{s['type']}[/bold]\n{s['value']}\n\n{suggest_fix(s)}",
                border_style="red"
            ))

    if leaks:
        console.print("\n[bold yellow]⚠️ Leaks Found:[/bold yellow]")
        for l in leaks:
            console.print(f"[yellow]- {l}[/yellow]")
def scan_path(path):
    path = os.path.abspath(path)  # ✅ convert to absolute path

    if os.path.isfile(path):
        scan_file(path)
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    scan_file(full_path)

def main():
    parser = argparse.ArgumentParser(description="SentinelCode AI")
    parser.add_argument("--path", required=True, help="File or folder to scan")

    args = parser.parse_args()


    scan_path(args.path)


if __name__ == "__main__":
    main()