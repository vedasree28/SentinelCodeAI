def get_severity(issue_type: str) -> str:
    if any(k in issue_type for k in ["Key", "Token", "Private", "URI"]):
        return "HIGH"
    elif any(k in issue_type for k in ["Suspicious", "Entropy"]):
        return "MEDIUM"
    return "LOW"