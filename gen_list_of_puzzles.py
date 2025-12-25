from pathlib import Path
import json
import argparse
import sys

#!/usr/bin/env python3
"""
Generate a JSON file listing all .json filenames in Site/puzzles.
Saves output to Site/puzzles/puzzles_list.json by default.
"""

def list_json_files(directory: Path):
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")
    return sorted([p.name for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.json'])

def make_lists_of_puzzles():
    p = argparse.ArgumentParser(description="Make a JSON of all .json filenames in Site/puzzles")
    p.add_argument("--dir", "-d", default=Path(__file__).parent / "Site" / "puzzles", help="Directory to scan")
    p.add_argument("--out", "-o", default=None, help="Output JSON file path")
    args = p.parse_args()

    directory = Path(args.dir)
    try:
        files = list_json_files(directory)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
        
    filters = [5, 10]
    paths = ["ArchipelagoPicross\\ArchipelagoPicross\\worlds\\picross\\data", "Site\\lists"]
    for p in paths:
        for f in filters:
            filesh = [fn for fn in files if fn.startswith(f"p_{f}_")]

            out_path = Path(f"{p}\\pl_{f}.json")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(filesh, indent=2, ensure_ascii=False), encoding="utf-8")
            print(str(out_path))

if __name__ == "__main__":
    make_lists_of_puzzles()