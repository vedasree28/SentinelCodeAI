import re
from typing import List, Dict

NLP_KEYWORDS = [
    ("password",       "MEDIUM"),
    ("secret",         "MEDIUM"),
    ("token",          "MEDIUM"),
    ("private",        "MEDIUM"),
    ("credential",     "MEDIUM"),
    ("api_key",        "MEDIUM"),
    ("auth",           "MEDIUM"),
    ("access_key",     "MEDIUM"),
    ("passphrase",     "MEDIUM"),
    ("encryption_key", "MEDIUM"),
    ("client_secret",  "MEDIUM"),
    ("bearer",         "MEDIUM"),
    ("session_token",  "MEDIUM"),
]

def detect_nlp(code: str) -> List[Dict]:
    findings = []
    lines = code.splitlines()
    for i, line in enumerate(lines, 1):
        lower = line.lower()
        if "=" not in line:
            continue
        for keyword, risk in NLP_KEYWORDS:
            if re.search(rf'\b{keyword}\b', lower):
                findings.append({
                    "type": "NLP Context",
                    "keyword": keyword,
                    "risk": risk,
                    "line": i,
                    "value": line.strip(),
                })
                break
    return findings
