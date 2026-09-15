"""Fix escaping in the one-time migration's generated structure checker."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "scripts" / "check_repo_structure.py"
text = path.read_text(encoding="utf-8")
needle = '''    if errors:\n        raise SystemExit("Repository structure check failed:\n- " + "\n- ".join(errors))\n'''
# The first migration accidentally materializes newlines inside the string literal.
broken = '''    if errors:\n        raise SystemExit("Repository structure check failed:\n- " + "\n- ".join(errors))\n'''.replace('\\n', '\n')
replacement = '''    if errors:\n        raise SystemExit("Repository structure check failed:\\n- " + "\\n- ".join(errors))\n'''
if broken in text:
    text = text.replace(broken, replacement)
elif needle not in text:
    # Rewrite the tail robustly if source formatting differs.
    marker = "    if errors:"
    start = text.index(marker)
    end = text.index('    print("Repository structure check passed")', start)
    text = text[:start] + replacement + text[end:]
path.write_text(text, encoding="utf-8")
Path(__file__).unlink()
