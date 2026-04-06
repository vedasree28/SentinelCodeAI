def suggest_fix(issue: dict) -> str:
    issue_type = issue.get("type")
    value = issue.get("value")

    if issue_type and ("Key" in issue_type or "Token" in issue_type):
        return f"""
Fix:
Move secret to environment variable

Example:
import os
SECRET = os.getenv("SECRET_KEY")

Detected:
{value}
"""

    if issue_type == "Suspicious Variable":
        return f"""
Fix:
Avoid hardcoding sensitive data

Detected:
{value}

Use:
import os
PASSWORD = os.getenv("PASSWORD")
"""

    if issue_type == "High Entropy String":
        return """
Fix:
Avoid storing random sensitive tokens in code.
Store them securely using environment variables or vaults.
"""

    return "Review this issue manually"