from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
MAX_IMAGE_COUNT = 325
MAX_SINGLE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 350 * 1024 * 1024


def main() -> int:
    images = sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in IMAGE_SUFFIXES
    )
    total = sum(path.stat().st_size for path in images)
    oversized = [path for path in images if path.stat().st_size > MAX_SINGLE_BYTES]
    errors: list[str] = []
    if len(images) > MAX_IMAGE_COUNT:
        errors.append(f"image count {len(images)} exceeds {MAX_IMAGE_COUNT}")
    if total > MAX_TOTAL_BYTES:
        errors.append(
            f"image bytes {total} exceed {MAX_TOTAL_BYTES}; move originals to release storage"
        )
    for path in oversized:
        errors.append(
            f"{path.relative_to(ROOT).as_posix()} is {path.stat().st_size} bytes; "
            f"single-image limit is {MAX_SINGLE_BYTES}"
        )
    if errors:
        print("Asset budget audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Asset budget passed: {len(images)} images, {total} bytes, "
        f"largest {max((path.stat().st_size for path in images), default=0)} bytes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
