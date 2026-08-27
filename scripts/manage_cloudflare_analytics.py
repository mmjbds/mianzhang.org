from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN = "2034c57ea32d4ea6b8d882fb2eb2b9c9"
BEACON_URL = "https://static.cloudflareinsights.com/beacon.min.js"
MARKER = "<!-- Cloudflare Web Analytics -->"
END_MARKER = "<!-- End Cloudflare Web Analytics -->"
SNIPPET = (
    f"{MARKER}\n"
    f"<script type='module' src='{BEACON_URL}' "
    f"data-cf-beacon='{{\"token\": \"{TOKEN}\"}}'></script>\n"
    f"{END_MARKER}"
)


def eligible_html(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.html"))
        if "</body>" in path.read_text(encoding="utf-8").lower()
    ]


def audit_file(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    lower = source.lower()
    errors: list[str] = []
    if lower.count("</body>") != 1:
        errors.append("expected exactly one </body>")
    if source.count(MARKER) != 1 or source.count(END_MARKER) != 1:
        errors.append("expected exactly one Cloudflare Analytics marker pair")
    if source.count(BEACON_URL) != 1:
        errors.append("expected exactly one Cloudflare beacon URL")
    if source.count(TOKEN) != 1:
        errors.append("expected exactly one configured beacon token")
    if SNIPPET not in source:
        errors.append("beacon snippet differs from the approved snippet")
    if source.find(SNIPPET) > lower.rfind("</body>"):
        errors.append("beacon appears after </body>")
    return errors


def inject(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    if SNIPPET in source:
        return False
    if MARKER in source or END_MARKER in source or BEACON_URL in source:
        raise ValueError(f"existing non-canonical Cloudflare snippet: {path}")
    body_index = source.lower().rfind("</body>")
    if body_index < 0:
        return False
    updated = source[:body_index].rstrip() + "\n" + SNIPPET + "\n" + source[body_index:]
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install or audit the approved Cloudflare Web Analytics beacon."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    pages = eligible_html(args.root)
    if args.check:
        failures: list[str] = []
        for path in pages:
            for error in audit_file(path):
                failures.append(f"{path.relative_to(args.root).as_posix()}: {error}")
        if failures:
            print("Cloudflare Web Analytics audit failed:")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print(f"Cloudflare Web Analytics audit passed: {len(pages)} HTML pages")
        return 0

    changed = sum(inject(path) for path in pages)
    print(f"Cloudflare Web Analytics installed: {changed} changed / {len(pages)} eligible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
