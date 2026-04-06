def suggest_fix(issue: dict) -> str:
    issue_type = issue.get("type")

    if issue_type in ["AWS Key", "Generic Token", "High Entropy String"]:
        return (
            "🔧 सुझाव:\n"
            "Move this secret to environment variables.\n"
            "Example:\n"
            "import os\n"
            "API_KEY = os.getenv('API_KEY')"
        )

    if "file" in issue_type.lower():
        return "🔧 सुझाव: Use 'with open(...) as f:' to auto-close files."

    return "🔧 General fix: Review and secure this code."