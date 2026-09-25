import ast, os, pytest

FORBIDDEN = {
    "domain": ["infrastructure", "api", "application", "interfaces", "modules"],
    "interfaces": ["infrastructure", "api", "modules"],
    "application": ["infrastructure", "api", "modules"],
}

def test_architecture_boundaries():
    violations = []
    for layer, forbidden in FORBIDDEN.items():
        layer_path = f"src/universal_ai/{layer}"
        if not os.path.exists(layer_path): continue
        for root, _, files in os.walk(layer_path):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        tree = ast.parse(f.read())                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            imports = [alias.name for alias in node.names]
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            imports = [node.module]
                        else: continue
                        for imp in imports:
                            for forb in forbidden:
                                if f"universal_ai.{forb}" in imp or imp.startswith(f"{forb}."):
                                    violations.append(f"{filepath} imports '{imp}'")
    assert not violations, "Architecture violations:\n" + "\n".join(violations)