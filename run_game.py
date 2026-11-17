import base64
import io
import os
import runpy
import zipfile
from pathlib import Path

# That Cat Game - mobile/PC launcher
# Install pygame first: pip install pygame

def main():
    here = Path(__file__).resolve().parent
    bundle_dir = here / "bundle"
    parts = []
    for i in range(1, 9):
        path = bundle_dir / f"part{i:02d}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Missing game data: {path.name}")
        parts.append(path.read_text(encoding="utf-8").strip())

    packed = base64.b64decode("".join(parts))
    game_dir = here / "_game"
    game_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(packed), "r") as zf:
        zf.extractall(game_dir)

    os.chdir(game_dir)
    runpy.run_path(str(game_dir / "main.py"), run_name="__main__")

if __name__ == "__main__":
    main()
