import ast
from typing import List

class ResourceVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        # Detect open() without close
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            self.issues.append(f"Possible unclosed file at line {node.lineno}")
        self.generic_visit(node)

def detect_leaks(file_path: str) -> List[str]:
    issues = []
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        visitor = ResourceVisitor()
        visitor.visit(tree)
        issues.extend(visitor.issues)

    except Exception as e:
        issues.append(f"Parsing error: {str(e)}")

    return issues