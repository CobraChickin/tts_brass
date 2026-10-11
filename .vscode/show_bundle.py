import json
import subprocess
import sys
from pathlib import Path

import build
import debug


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "global"
    save_path = build.get_output_folder() / f"{build.GAME_NAME}.json"

    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if target.lower() == "global":
        script = data.get("LuaScript", "")
    else:
        script = debug.find_script(data.get("ObjectStates", []), target)

    if not script:
        print(f"No bundled script found for '{target}' in {save_path}")
        sys.exit(1)

    temp_dir = Path(__file__).parent / "temp"
    temp_dir.mkdir(exist_ok=True)
    out_path = temp_dir / f"bundled_{target}.ttslua"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(script)

    print(f"Wrote {out_path}")
    subprocess.run(["code", "-r", str(out_path)], shell=True)


if __name__ == "__main__":
    main()
