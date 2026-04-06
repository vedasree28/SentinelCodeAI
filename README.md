# SentinelCode AI 🚀

SentinelCode AI is a proactive developer tool that scans your code **before it is committed** to detect:

* 🔐 Hardcoded secrets (API keys, tokens, credentials)
* ⚠️ Resource leaks (unclosed files, improper handling)
* 🧠 Context-based vulnerabilities

It integrates with Git pre-commit hooks to **block unsafe commits and improve code quality automatically**.

---

## ✨ Features

* 🔍 Regex + entropy-based secret detection
* 🧠 Context-aware detection (sensitive variable names)
* ⚙️ AST-based memory leak detection
* 🔒 Git pre-commit hook integration
* 💡 Smart fix suggestions
* 🎨 Clean and colorful CLI output (Rich UI)
* 📁 Supports both file and folder scanning

---

## 🚀 Setup

### 🔹 Option A — Install as CLI tool (Recommended)

```bash
pip install -e .
```

👉 Enables the global `sentinel` command.

---

### 🔹 Option B — Without pip install

```bash
pip install -r requirements.txt
python install_hook.py
```

---

## 🔍 Usage

### 📄 Scan a single file

```bash
sentinel --path path/to/file.py
```

---

### 📁 Scan an entire folder

```bash
sentinel --path path/to/folder/
```

---

### 🛠️ Without pip install

```bash
python -m src.cli.main --path path/to/file_or_folder
```

---

## 🔐 Pre-commit Hook Workflow

Once installed, every Git commit is automatically intercepted:

```
git commit -m "my changes"
      ↓
SentinelCode AI scans staged files
      ↓
HIGH risk found  → ❌ Commit BLOCKED + report shown
No issues        → ✅ Commit allowed
```

---

## 🧪 Run Tests

```bash
python -m pytest tests/
```

---

## 📌 Example Output

```
🔍 Scanning: tests/test_secret.py

🔐 Secrets Found:

[HIGH] AWS Access Key → AKIA1234567890ABCDEF
Fix:
Move secret to environment variable

Example:
import os
SECRET = os.getenv("SECRET_KEY")

⚠️ Leaks Found:
- Possible unclosed file at line 7
```

---

## 🏗️ Project Structure

```
SentinelCodeAI/
│
├── src/
│   ├── core/
│   │   ├── secrets.py
│   │   ├── leaks.py
│   │   ├── severity.py
│   │
│   ├── ai/
│   │   ├── fixer.py
│   │
│   ├── cli/
│   │   ├── main.py
│   │
│   ├── git_hooks/
│       ├── pre_commit.py
│
├── tests/
│   ├── test_secrets.py
│
├── requirements.txt
├── setup.py
├── install_hook.py
└── README.md
```

---

## 🚀 Future Improvements

* 🔧 Auto-fix engine (automatic code correction)
* 🛡️ Integration with security tools (Bandit, Semgrep)
* 🌐 Web dashboard for scan history
* 🌍 Multi-language support

---

## 💡 Why SentinelCode AI?

* Prevents accidental exposure of secrets
* Improves code quality before commit
* Saves debugging time by catching issues early
* Acts as a lightweight local security layer

---

## 👩‍💻 Author

**A. Veda Sree**

---

## ⭐ Contribute

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📜 License

This project is open-source and available under the MIT License.
