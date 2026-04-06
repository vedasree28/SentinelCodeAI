import ast
from typing import List

class ResourceVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            parent = getattr(node, 'parent', None)
            if not isinstance(parent, ast.withitem):
                self.issues.append(f"Possible unclosed file at line {node.lineno}")
        self.generic_visit(node)

def add_parent_links(node):
    for child in ast.iter_child_nodes(node):
        setattr(child, 'parent', node)
        add_parent_links(child)

def detect_leaks(file_path: str) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read())

        add_parent_links(tree)

        visitor = ResourceVisitor()
        visitor.visit(tree)

        return visitor.issues

    except Exception:
        return []