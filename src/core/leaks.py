import ast
import os
import re
from typing import List

# ─── Python AST Engine ────────────────────────────────────────────────────────

class ResourceVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def _is_in_with(self, node) -> bool:
        parent = getattr(node, 'parent', None)
        while parent:
            if isinstance(parent, ast.With):
                return True
            parent = getattr(parent, 'parent', None)
        return False

    def visit_Call(self, node):
        func = node.func

        # open() without with block
        if isinstance(func, ast.Name) and func.id == "open":
            if not self._is_in_with(node):
                self.issues.append(f"Possible unclosed file at line {node.lineno}")

        # threading.Lock() acquired but never used as context manager
        if isinstance(func, ast.Attribute) and func.attr == "Lock":
            if not self._is_in_with(node):
                self.issues.append(f"threading.Lock() not used as context manager at line {node.lineno}")

        # subprocess.Popen() without context manager or .wait()
        if isinstance(func, ast.Attribute) and func.attr == "Popen":
            if not self._is_in_with(node):
                self.issues.append(f"subprocess.Popen() without context manager at line {node.lineno}")

        self.generic_visit(node)


def add_parent_links(node):
    for child in ast.iter_child_nodes(node):
        setattr(child, 'parent', node)
        add_parent_links(child)


def _detect_python_ast(file_path: str) -> List[str]:
    try:
        safe_path = os.path.realpath(file_path)
        if not os.path.isfile(safe_path):
            return []
        with open(safe_path, "r", encoding="utf-8", errors="ignore") as f:  # nosec
            source = f.read()
        tree = ast.parse(source)
        add_parent_links(tree)
        visitor = ResourceVisitor()
        visitor.visit(tree)
        return visitor.issues
    except Exception:
        return []


# ─── Regex-based Multi-language Engine ───────────────────────────────────────

REGEX_PATTERNS = {
    # Python
    "python": [
        ("python_unclosed_db",     r'(?i)(psycopg2|pymysql|sqlite3|cx_Oracle|pyodbc)\.connect\('),
        ("python_unclosed_socket", r'socket\.socket\('),
        ("python_unclosed_session",r'requests\.Session\('),
    ],
    # C / C++
    "c": [
        ("cpp_malloc_no_free",  r'\bmalloc\s*\('),
        ("cpp_new_no_delete",   r'\bnew\b'),
        ("cpp_fopen_no_fclose", r'\bfopen\s*\('),
    ],
    # Java
    "java": [
        ("java_unclosed_stream",     r'new\s+(FileInputStream|FileOutputStream|BufferedReader|BufferedWriter|InputStreamReader|OutputStreamWriter)\s*\('),
        ("java_unclosed_connection", r'DriverManager\.getConnection\s*\('),
    ],
    # JavaScript / TypeScript
    "js": [
        ("js_unclosed_fs",       r'fs\.open\s*\('),
        ("js_event_listener",    r'addEventListener\s*\('),
    ],
    # Go
    "go": [
        ("go_unclosed_file",  r'os\.Open\s*\('),
        ("go_unclosed_http",  r'http\.Get\s*\('),
    ],
    # Rust
    "rust": [
        ("rust_unclosed_file", r'File::open\s*\('),
        ("rust_raw_pointer",   r'\*mut\s+\w+'),
    ],
}

EXT_MAP = {
    ".py":   "python",
    ".c":    "c",   ".cpp": "c", ".cc": "c", ".h": "c",
    ".java": "java",
    ".js":   "js",  ".ts":  "js", ".jsx": "js", ".tsx": "js",
    ".go":   "go",
    ".rs":   "rust",
}


def _detect_regex(file_path: str) -> List[str]:
    safe_path = os.path.realpath(file_path)
    if not os.path.isfile(safe_path):
        return []
    ext = os.path.splitext(safe_path)[1].lower()
    lang = EXT_MAP.get(ext)
    if not lang:
        return []

    try:
        with open(safe_path, "r", encoding="utf-8", errors="ignore") as f:  # nosec
            lines = f.readlines()
    except OSError:
        return []

    issues = []
    for pattern_name, pattern in REGEX_PATTERNS.get(lang, []):
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):  # nosec
                issues.append(f"[{pattern_name}] Possible resource leak at line {i}")

    return issues


# ─── Public API ───────────────────────────────────────────────────────────────

def detect_leaks(file_path: str) -> List[str]:
    file_path = os.path.realpath(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".py":
        return _detect_python_ast(file_path) + _detect_regex(file_path)
    return _detect_regex(file_path)
