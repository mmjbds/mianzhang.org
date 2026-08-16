from __future__ import annotations

import argparse
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://mianzhang.org"
PUBLIC_FILE_SUFFIXES = {".html", ".json", ".jsonl", ".md", ".pdf", ".txt", ".xml"}
DIRECT_PUBLIC_FILES = {"llms.txt", "robots.txt", "sitemap.xml"}
EXCLUDED_PREFIXES = (".github/", "scripts/")
INDEXABLE_NON_HTML_PREFIXES = (
    "ai-agent-reliability/",
    "demos/reflexbench-observer-depth/",
    "papers/kdd-2026/",
    "papers/public_index/",
    "public_registry/",
    "registries/",
)
EXCLUDED_DOC_PREFIXES = (
    "docs/baidu-url-list-",
    "docs/google-bing-url-list-",
    "docs/indexnow-submission-receipt-",
    "docs/indexnow-url-list-",
)


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical = ""
        self.noindex = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "link" and "canonical" in values.get("rel", "").lower():
            self.canonical = values.get("href", "").strip()
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.noindex = "noindex" in values.get("content", "").lower()


def sitemap_urls() -> set[str]:
    root = ElementTree.parse(ROOT / "sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        node.text.strip()
        for node in root.findall("sm:url/sm:loc", namespace)
        if node.text and node.text.strip()
    }


def changed_paths(before: str, after: str) -> list[str]:
    if not before or set(before) == {"0"}:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", before, after],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def route_for_file(relative: str, canonical_urls: set[str]) -> str | None:
    if relative in DIRECT_PUBLIC_FILES:
        return f"{ORIGIN}/{relative}"
    if relative.startswith(EXCLUDED_PREFIXES) or relative.startswith(EXCLUDED_DOC_PREFIXES):
        return None
    path = ROOT / relative
    if not path.is_file() or path.suffix.lower() not in PUBLIC_FILE_SUFFIXES:
        return None
    if path.suffix.lower() == ".html":
        parser = MetadataParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if parser.noindex or parser.canonical not in canonical_urls:
            return None
        return parser.canonical
    if not relative.startswith(INDEXABLE_NON_HTML_PREFIXES):
        return None
    return f"{ORIGIN}/{relative}"


def build_urls(before: str, after: str, include_all: bool) -> list[str]:
    canonical_urls = sitemap_urls()
    if include_all or not before or set(before) == {"0"}:
        return sorted(canonical_urls | {f"{ORIGIN}/llms.txt", f"{ORIGIN}/sitemap.xml"})
    routes = {
        route
        for relative in changed_paths(before, after)
        if (route := route_for_file(relative, canonical_urls))
    }
    return sorted(routes)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a host-specific IndexNow list from a git change set."
    )
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    urls = build_urls(args.before, args.after, args.all)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(f"{url}\n" for url in urls), encoding="utf-8")
    print(f"wrote {len(urls)} URLs to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
