# src/ai/fixer.py

import html
from src.ai.rules import FIX_RULES


def suggest_fix(issue: dict) -> str:
    issue_type = html.escape(issue.get("type", "Unknown Issue"))
    value = html.escape(issue.get("value", ""))

    # 🔥 Get rule dynamically
    rule = FIX_RULES.get(issue_type)

    # 🧠 Default fallback rule
    if not rule:
        return (
            f"Issue: {issue_type}\nSeverity: LOW\n\nDetected:\n{value}\n\nFix:\nNo predefined rule found. Review manually."
        )

    severity = rule.get("severity", "LOW")
    fix = rule.get("fix", "")
    example = rule.get("example", "")
    explanation = rule.get("explanation", "")

    # 🧠 Context-aware hints
    context_hint = generate_context_hint(value)

    return (
        f"Issue: {issue_type}\nSeverity: {severity}\n\nWhy this matters:\n{explanation}"
        f"\n\nDetected:\n{value}\n\nFix:\n{fix}\n\nExample:\n{example}\n\nContext Hint:\n{context_hint}"
    )
def generate_context_hint(value: str) -> str:
    hints = {
        "password": "Use hashed passwords (bcrypt) instead of storing plain text.",
        "token": "Rotate tokens regularly and store them securely.",
        "secret": "Use a secrets manager like AWS Secrets Manager.",
        "api_key": "Restrict API key permissions and use environment variables.",
        "apikey": "Restrict API key permissions and use environment variables.",
        "open(": "Use 'with open(...) as f:' to avoid resource leaks.",
    }
    safe_value = html.escape(value).lower()
    for keyword, hint in hints.items():
        if keyword in safe_value:
            return hint
    return "Follow secure coding best practices."