from __future__ import annotations

import argparse
from collections import defaultdict
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
BASE_URL = "https://mianzhang.org"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
RELEASE_DATE = "2026-08-17"
LASTMOD_OVERRIDES = {
    f"{BASE_URL}/": RELEASE_DATE,
    f"{BASE_URL}/docs/external-submission-status-2026-06-15.html": RELEASE_DATE,
    f"{BASE_URL}/docs/public-completion-audit-2026-06-15.html": RELEASE_DATE,
    f"{BASE_URL}/docs/search-discovery-2026-06-15.html": RELEASE_DATE,
    f"{BASE_URL}/docs/search-index-weekly-report-2026-06-15.html": RELEASE_DATE,
    f"{BASE_URL}/docs/search-submission-status-current.html": RELEASE_DATE,
    f"{BASE_URL}/registries/claim_to_evidence_table_v0.html": RELEASE_DATE,
    f"{BASE_URL}/registries/schema_notes_v0.html": RELEASE_DATE,
}

VERIFICATION_FILES = {
    "google9c7439a09f492752.html",
    "googlee95cf06405c388af.html",
}


class CanonicalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical = ""

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "link" and "canonical" in values.get("rel", "").lower():
            self.canonical = values.get("href", "").strip()


def collect_canonical_pages(existing: dict[str, str]) -> dict[str, str]:
    canonical_files: dict[str, list[str]] = defaultdict(list)
    for path in sorted(ROOT.rglob("*.html")):
        if path.parent == ROOT and path.name in VERIFICATION_FILES:
            continue
        parser = CanonicalParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if not parser.canonical:
            raise ValueError(f"missing canonical: {path.relative_to(ROOT)}")
        parsed = urlsplit(parser.canonical)
        if parsed.scheme != "https" or parsed.netloc != urlsplit(BASE_URL).netloc:
            raise ValueError(
                f"canonical outside {BASE_URL}: {path.relative_to(ROOT)} -> "
                f"{parser.canonical}"
            )
        canonical_files[parser.canonical].append(path.relative_to(ROOT).as_posix())

    duplicates = {
        canonical: paths
        for canonical, paths in canonical_files.items()
        if len(paths) > 1
    }
    if duplicates:
        detail = "; ".join(
            f"{canonical}: {', '.join(paths)}"
            for canonical, paths in sorted(duplicates.items())
        )
        raise ValueError(f"duplicate canonical pages: {detail}")

    return {
        canonical: LASTMOD_OVERRIDES.get(
            canonical, existing.get(canonical, RELEASE_DATE)
        )
        for canonical in canonical_files
    }


def load_entries() -> dict[str, str]:
    root = ElementTree.parse(SITEMAP).getroot()
    existing: dict[str, str] = {}
    for node in root.findall(f"{{{NAMESPACE}}}url"):
        loc = node.findtext(f"{{{NAMESPACE}}}loc", default="").strip()
        lastmod = node.findtext(f"{{{NAMESPACE}}}lastmod", default="").strip()
        if not loc:
            continue
        existing[loc] = lastmod
    return collect_canonical_pages(existing)


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
        description=(
            "Build the public sitemap from independently canonical HTML pages."
        )
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
