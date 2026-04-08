import re
import math
from typing import List, Dict, Set

# 🔐 Strong + Expanded Patterns
SECRET_PATTERNS = [
    # Cloud - AWS
    ("AWS Access Key", r'AKIA[0-9A-Z]{16}'),
    ("AWS Secret Key", r'(?i)aws(.{0,20})?(secret|access)?(.{0,20})?[0-9a-zA-Z/+]{40}'),

    # Cloud - GCP
    ("Google API Key", r'AIza[0-9A-Za-z\-_]{35}'),
    ("GCP Service Account", r'"type":\s*"service_account"'),

    # Cloud - Azure
    ("Azure Storage Key", r'(?i)DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{88}'),
    ("Azure Client Secret", r'(?i)(client_secret|AZURE_CLIENT_SECRET)[\s:=\'"]+[A-Za-z0-9\-_~.]{34,}'),
    ("Azure SAS Token", r'sv=\d{4}-\d{2}-\d{2}&s[a-z]='),

    # DevOps
    ("GitHub Token", r'ghp_[A-Za-z0-9]{36}'),
    ("GitHub OAuth Token", r'gho_[A-Za-z0-9]{36}'),
    ("GitLab Token", r'glpat-[A-Za-z0-9\-_]{20}'),

    # Payments
    ("Stripe Secret Key", r'sk_live_[0-9a-zA-Z]{24}'),
    ("Stripe Public Key", r'pk_live_[0-9a-zA-Z]{24}'),
    ("Twilio Account SID", r'AC[a-zA-Z0-9]{32}'),
    ("Twilio Auth Token", r'(?i)twilio(.{0,20})?[a-f0-9]{32}'),
    ("SendGrid API Key", r'SG\.[A-Za-z0-9\-_]{22}\.[A-Za-z0-9\-_]{43}'),

    # Auth
    ("JWT Token", r'eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'),

    # Database
    ("MongoDB URI", r'mongodb(\+srv)?:\/\/[^\s]+'),
    ("PostgreSQL URI", r'postgres:\/\/[^\s]+'),
    ("MySQL URI", r'mysql:\/\/[^:]+:[^@]+@[^\s]+'),

    # .env style assignments
    ("Dotenv Secret", r'(?mi)^(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY|ACCESS_KEY|CLIENT_SECRET)=[^\s]+'),

    # Private Keys
    ("Private Key", r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----'),

    # Messaging
    ("Slack Token", r'xox[baprs]-[A-Za-z0-9-]{10,}'),

    # Generic (Improved)
    ("Generic API Key", r'(?i)(api[_-]?key|token|secret)[\'"\s:=]+[A-Za-z0-9\-_]{16,}')
]

# 🔍 Suspicious variable names
SUSPICIOUS_NAMES = [
    "api_key", "apikey", "secret", "token",
    "password", "passwd", "pwd",
    "auth", "credential", "access_key",
    "encryption_key", "client_secret", "bearer", "session_token",
    "private_key", "passphrase"
]

# 🚫 False positive filter
def is_false_positive(value: str) -> bool:
    safe_words = ["example", "test", "dummy", "sample", "localhost"]
    return any(word in value.lower() for word in safe_words)

# 🔢 Entropy calculation
def shannon_entropy(data: str) -> float:
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    return -sum([p * math.log2(p) for p in prob])

# 🔐 Main detection
def detect_secrets(code: str) -> List[Dict]:
    findings = []
    seen: Set[str] = set()  # ✅ Deduplication

    # 1️⃣ Regex-based detection
    for name, pattern in SECRET_PATTERNS:
        matches = re.findall(pattern, code)
        for match in matches:
            value = match if isinstance(match, str) else match[0]

            if is_false_positive(value):
                continue

            key = f"{name}:{value}"
            if key in seen:
                continue
            seen.add(key)

            findings.append({
                "type": name,
                "value": value,
                "confidence": "HIGH",
                "method": "regex"
            })

    # 2️⃣ Context-based detection
    lines = code.split("\n")
    for i, line in enumerate(lines):
        lower_line = line.lower()

        for keyword in SUSPICIOUS_NAMES:
            if keyword in lower_line and "=" in line:
                value = line.strip()

                if is_false_positive(value):
                    continue

                key = f"context:{value}"
                if key in seen:
                    continue
                seen.add(key)

                findings.append({
                    "type": "Suspicious Variable",
                    "value": value,
                    "confidence": "MEDIUM",
                    "line": i + 1,
                    "method": "context"
                })

    # 3️⃣ Entropy-based detection
    tokens = re.findall(r'[A-Za-z0-9+/=]{20,}', code)
    for token in tokens:
        if is_false_positive(token):
            continue

        entropy = shannon_entropy(token)

        if entropy > 4.8:  # 🔥 tuned threshold
            key = f"entropy:{token}"
            if key in seen:
                continue
            seen.add(key)

            findings.append({
                "type": "High Entropy String",
                "value": token,
                "confidence": "MEDIUM",
                "method": "entropy"
            })

    return findings