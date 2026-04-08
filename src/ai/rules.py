# src/ai/rules.py

FIX_RULES = {

    # ☁️ Cloud Keys
    "AWS Access Key": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Move AWS key to environment variable",
        "example": 'AWS_KEY = os.getenv("AWS_ACCESS_KEY")',
        "explanation": "Hardcoding AWS keys can expose your cloud infrastructure."
    },

    "AWS Secret Key": {
        "severity": "CRITICAL",
        "priority": 1,
        "fix": "Store AWS secret key securely",
        "example": 'AWS_SECRET = os.getenv("AWS_SECRET_KEY")',
        "explanation": "AWS secret keys allow full access and must never be exposed."
    },

    "Google API Key": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Store API key in environment variables",
        "example": 'GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")',
        "explanation": "Google API keys can be abused if leaked."
    },

    # 🔧 DevOps / Tokens
    "GitHub Token": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Revoke and regenerate token immediately",
        "example": 'GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")',
        "explanation": "GitHub tokens allow repository access and must be secured."
    },

    "GitHub OAuth Token": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Store OAuth tokens securely",
        "example": 'OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")',
        "explanation": "OAuth tokens can be used for authentication and must be protected."
    },

    "GitLab Token": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Move token to secure storage",
        "example": 'GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")',
        "explanation": "GitLab tokens grant access to repositories and APIs."
    },

    # 💳 Payment
    "Stripe Secret Key": {
        "severity": "CRITICAL",
        "priority": 1,
        "fix": "Never expose Stripe secret keys",
        "example": 'STRIPE_SECRET = os.getenv("STRIPE_SECRET")',
        "explanation": "Stripe secret keys can be used to perform financial transactions."
    },

    "Stripe Public Key": {
        "severity": "LOW",
        "priority": 3,
        "fix": "Public keys are usually safe but avoid misuse",
        "example": 'STRIPE_PUBLIC = os.getenv("STRIPE_PUBLIC")',
        "explanation": "Public keys are generally safe but should still be handled properly."
    },

    # 🔐 Authentication
    "JWT Token": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Generate tokens dynamically at runtime",
        "example": "token = generate_jwt(user)",
        "explanation": "JWT tokens should not be hardcoded as they can be reused."
    },

    # 🗄️ Database
    "MongoDB URI": {
        "severity": "CRITICAL",
        "priority": 1,
        "fix": "Move DB credentials to environment variables",
        "example": 'MONGO_URI = os.getenv("MONGO_URI")',
        "explanation": "Database URIs may contain usernames and passwords."
    },

    "PostgreSQL URI": {
        "severity": "CRITICAL",
        "priority": 1,
        "fix": "Store DB connection string securely",
        "example": 'DB_URI = os.getenv("DATABASE_URL")',
        "explanation": "Database credentials should never be exposed in code."
    },

    # 🔑 Keys
    "Private Key": {
        "severity": "CRITICAL",
        "priority": 1,
        "fix": "Remove private key immediately",
        "example": "Store in secure vault (AWS Secrets Manager)",
        "explanation": "Private keys must never be committed to source control."
    },

    # 💬 Messaging / APIs
    "Slack Token": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Revoke and rotate Slack token",
        "example": 'SLACK_TOKEN = os.getenv("SLACK_TOKEN")',
        "explanation": "Slack tokens can allow unauthorized access to workspace data."
    },

    # 🔧 Generic
    "Generic API Key": {
        "severity": "HIGH",
        "priority": 1,
        "fix": "Store API keys securely",
        "example": 'API_KEY = os.getenv("API_KEY")',
        "explanation": "API keys should not be hardcoded in source code."
    },

    # ⚠️ Medium Risk
    "Suspicious Variable": {
        "severity": "MEDIUM",
        "priority": 2,
        "fix": "Avoid storing sensitive values directly",
        "example": 'PASSWORD = os.getenv("PASSWORD")',
        "explanation": "Variables like password/token may expose secrets if hardcoded."
    },

    "High Entropy String": {
        "severity": "MEDIUM",
        "priority": 2,
        "fix": "Verify and secure if sensitive",
        "example": "Move to environment variable if needed",
        "explanation": "High entropy strings often indicate encoded secrets."
    },

    # 🧠 Memory / Resource Leaks
    "Unclosed File": {
        "severity": "LOW",
        "priority": 3,
        "fix": "Use context manager",
        "example": "with open('file.txt') as f:",
        "explanation": "Unclosed files can cause memory leaks."
    },

    "Unclosed DB Connection": {
        "severity": "MEDIUM",
        "priority": 2,
        "fix": "Close DB connection properly",
        "example": "conn.close()",
        "explanation": "Unclosed DB connections can exhaust resources."
    }
}