"""Build an isolated GitHub Pages artifact with Python's standard library."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
output = root / "_site"
if output.exists():
    shutil.rmtree(output)
output.mkdir()
for name in ("index.html", "styles.css", "script.js"):
    shutil.copy2(root / name, output / name)
(output / "assets").mkdir()
shutil.copy2(root / "assets/favicon.svg", output / "assets/favicon.svg")
(output / ".nojekyll").touch()
print(f"Static site built: {output}")
