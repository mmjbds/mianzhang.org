from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
BASE_URL = "https://mianzhang.org"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
RELEASE_DATE = "2026-08-16"

EXCLUDED_PREFIXES = (
    f"{BASE_URL}/.github/",
    f"{BASE_URL}/docs/google-bing-url-list-",
    f"{BASE_URL}/docs/indexnow-submission-receipt-",
    f"{BASE_URL}/docs/indexnow-url-list-",
)

ADDITIONAL_PUBLIC_FILES = (
    "COMMUNITY.md",
    "CONTENT_AND_MEDIA_LICENSE.md",
    "GOVERNANCE.md",
    "OPEN_SOURCE_BOUNDARY.md",
    "ROADMAP.md",
)


def load_entries() -> dict[str, str]:
    root = ElementTree.parse(SITEMAP).getroot()
    entries: dict[str, str] = {}
    for node in root.findall(f"{{{NAMESPACE}}}url"):
        loc = node.findtext(f"{{{NAMESPACE}}}loc", default="").strip()
        lastmod = node.findtext(f"{{{NAMESPACE}}}lastmod", default="").strip()
        if not loc or any(loc.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        entries[loc] = lastmod

    for relative in ADDITIONAL_PUBLIC_FILES:
        if not (ROOT / relative).is_file():
            raise FileNotFoundError(f"missing public sitemap target: {relative}")
        entries.setdefault(f"{BASE_URL}/{relative}", RELEASE_DATE)
    return entries


def render(entries: dict[str, str]) -> str:
    lines = [
        "<?xml version='1.0' encoding='utf-8'?>",
        f'<urlset xmlns="{NAMESPACE}">',
    ]
    for loc in sorted(entries, key=lambda value: (value != f"{BASE_URL}/", value)):
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(loc)}</loc>",
                f"    <lastmod>{escape(entries[loc])}</lastmod>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the public search sitemap without CI files or submission receipts."
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = render(load_entries())
    current = SITEMAP.read_text(encoding="utf-8")
    if args.check:
        if current != expected:
            print("sitemap.xml is stale; run python scripts/build_search_sitemap.py")
            return 1
        print(f"sitemap check passed: {expected.count('<url>')} URLs")
        return 0

    SITEMAP.write_text(expected, encoding="utf-8", newline="\n")
    print(f"wrote sitemap.xml: {expected.count('<url>')} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
