"""Convert the official IP102 classification archive to ImageFolder directories."""

from __future__ import annotations

import argparse
import re
import shutil
import tarfile
from pathlib import Path


def find_file(root: Path, name: str) -> Path:
    matches = list(root.rglob(name))
    if not matches:
        raise FileNotFoundError(f"Could not find {name} inside {root}")
    return matches[0]


def read_classes(path: Path) -> list[str]:
    names = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            match = re.match(r"^\s*\d+\s+(.*)$", line)
            names.append(match.group(1).strip() if match else line)
    return names


def read_split(path: Path) -> list[tuple[str, int]]:
    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and parts[-1].isdigit():
            records.append((" ".join(parts[:-1]), int(parts[-1])))
    if not records:
        raise ValueError(f"No filename/label records found in {path}")
    return records


def locate_image(root: Path, relative_name: str) -> Path:
    direct = root / relative_name
    if direct.exists():
        return direct
    matches = list(root.rglob(Path(relative_name).name))
    if not matches:
        raise FileNotFoundError(f"Could not locate image {relative_name}")
    return matches[0]


def export_split(records: list[tuple[str, int]], source_root: Path, output_root: Path, classes: list[str], split: str) -> int:
    copied = 0
    for filename, label in records:
        source = locate_image(source_root, filename)
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", classes[label]).strip("_")
        target_dir = output_root / split / f"{label:03d}_{safe_name}"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_dir / source.name)
        copied += 1
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare IP102 for CropSentinel training")
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/ip102"))
    args = parser.parse_args()
    extract_dir = args.output_dir.parent / "ip102_extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    if not any(extract_dir.iterdir()):
        with tarfile.open(args.archive) as archive:
            archive.extractall(extract_dir)
    classes = read_classes(find_file(extract_dir, "classes.txt"))
    image_root = next((path for path in [extract_dir / "images", extract_dir / "Image", extract_dir / "JPEGImages"] if path.exists()), extract_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for split in ["train", "val", "test"]:
        summary[split] = export_split(read_split(find_file(extract_dir, f"{split}.txt")), image_root, args.output_dir, classes, split)
    (args.output_dir / "class_names.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")
    print(f"Prepared {len(classes)} classes: {summary}")


if __name__ == "__main__":
    main()