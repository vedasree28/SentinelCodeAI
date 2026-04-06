def get_severity(issue_type: str) -> str:
    high = ["AWS Key", "Mongo URI"]
    medium = ["Generic Token", "High Entropy String"]
    low = ["Leak"]

    if issue_type in high:
        return "HIGH"
    elif issue_type in medium:
        return "MEDIUM"
    else:
        return "LOW"