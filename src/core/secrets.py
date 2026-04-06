import re
import math
from typing import List, Dict

# 🔹 Regex patterns
SECRET_PATTERNS = [
    ("AWS Key", r'AKIA[0-9A-Z]{16}'),
    ("Generic Token", r'\b[A-Za-z0-9]{32,}\b'),
    ("Mongo URI", r'mongodb://[A-Za-z0-9]+:[A-Za-z0-9]+@')
]

# 🔹 Entropy calculation
def shannon_entropy(data: str) -> float:
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    return -sum([p * math.log2(p) for p in prob])

# 🔹 Detect secrets
def detect_secrets(code: str) -> List[Dict]:
    findings = []

    # Regex detection
    for name, pattern in SECRET_PATTERNS:
        matches = re.findall(pattern, code)
        for match in matches:
            findings.append({
                "type": name,
                "value": match,
                "method": "regex"
            })

    # Entropy detection
    tokens = re.findall(r'[A-Za-z0-9+/=]{20,}', code)
    for token in tokens:
        entropy = shannon_entropy(token)
        if entropy > 4.5:  # threshold
            findings.append({
                "type": "High Entropy String",
                "value": token,
                "method": "entropy"
            })

    return findings