from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://mianzhang.org"
PUBLIC_PAGES = (
    "ai-agent-reliability/index.html",
    "demos/reflexbench-observer-depth/index.html",
    "zh/ai-agent-reliability/index.html",
)
EXPECTED_ROUTES = (
    "/ai-agent-reliability/",
    "/demos/reflexbench-observer-depth/",
    "/zh/ai-agent-reliability/",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.links.append(values["src"])


def local_target(route: str) -> Path:
    path = unquote(urlparse(route).path).lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    return ROOT / path


def main() -> int:
    errors: list[str] = []

    for rel in PUBLIC_PAGES:
        page = ROOT / rel
        if not page.is_file():
            errors.append(f"missing public page: {rel}")
            continue
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        base = f"{ORIGIN}/{rel}"
        for raw_link in parser.links:
            if raw_link.startswith(("mailto:", "tel:", "data:", "javascript:", "#")):
                continue
            absolute = urljoin(base, raw_link)
            parsed = urlparse(absolute)
            if parsed.netloc != "mianzhang.org":
                continue
            target = local_target(absolute)
            if not target.is_file():
                errors.append(f"{rel}: missing target for {raw_link}: {target.relative_to(ROOT)}")

    facts_path = ROOT / "ai-agent-reliability" / "facts.json"
    try:
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
        if facts.get("schema") != "ai_agent_reliability_public_facts_v1":
            errors.append("facts.json: unexpected schema")
        if len(facts.get("routes", [])) != 4:
            errors.append("facts.json: expected four reliability routes")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"facts.json: {exc}")

    try:
        sitemap = ElementTree.parse(ROOT / "sitemap.xml")
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {node.text for node in sitemap.findall(".//sm:loc", namespace)}
        for route in EXPECTED_ROUTES:
            url = f"{ORIGIN}{route}"
            if url not in locations:
                errors.append(f"sitemap.xml: missing {url}")
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f"sitemap.xml: {exc}")

    rows = []
    try:
        dataset = ROOT / "demos" / "reflexbench-observer-depth" / "reflexbench.jsonl"
        rows = [json.loads(line) for line in dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"reflexbench.jsonl: {exc}")
    if rows and (len(rows) != 20 or len({row.get("id") for row in rows}) != 20):
        errors.append("reflexbench.jsonl: expected 20 unique scenario records")

    if errors:
        print("Reliability route audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Reliability route audit passed: 3 HTML sitemap routes, 20 scenarios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
