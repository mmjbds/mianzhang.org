from __future__ import annotations

import json
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_FILES = {
    "google9c7439a09f492752.html",
    "googlee95cf06405c388af.html",
}
PRIORITY_PAGES = {
    "zh/index.html",
    "zh/embodied-ai-failure-learning/index.html",
    "essays/index.html",
    "zh/ai-trading-bot-risk-controls/index.html",
    "press/index.html",
    "docs/public-completion-audit-2026-06-15.html",
}
PRIORITY_MIN_DESCRIPTION_LENGTH = 120


class HeadMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self._in_json_ld = False
        self._json_parts: list[str] = []
        self.json_ld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta[key.lower()] = values.get("content", "")
        elif tag == "link" and "canonical" in values.get("rel", "").lower():
            self.canonical = values.get("href", "")
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld_blocks.append("".join(self._json_parts))
            self._in_json_ld = False


def main() -> int:
    errors: list[str] = []
    descriptions: dict[str, list[str]] = defaultdict(list)
    html_files = sorted(ROOT.rglob("*.html"))

    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel in VERIFICATION_FILES:
            continue

        source = path.read_text(encoding="utf-8")
        parser = HeadMetadataParser()
        parser.feed(source)
        description = parser.meta.get("description", "").strip()

        if not description:
            errors.append(f"{rel}: 缺少 meta description")
        else:
            descriptions[description].append(rel)
        if not parser.canonical:
            errors.append(f"{rel}: 缺少 canonical")

        for block in parser.json_ld_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: JSON-LD 无法解析: {exc}")

        if rel in PRIORITY_PAGES:
            if len(description) < PRIORITY_MIN_DESCRIPTION_LENGTH:
                errors.append(
                    f"{rel}: description 只有 {len(description)} 字符，"
                    f"低于 {PRIORITY_MIN_DESCRIPTION_LENGTH}"
                )
            metadata_descriptions = {
                description,
                parser.meta.get("og:description", "").strip(),
                parser.meta.get("twitter:description", "").strip(),
            }
            if "" in metadata_descriptions or len(metadata_descriptions) != 1:
                errors.append(f"{rel}: description、Open Graph 与 Twitter 摘要不一致")

        if '["??' in source or '"?? AI' in source:
            errors.append(f"{rel}: 结构化数据包含乱码占位符")

    for description, paths in descriptions.items():
        if len(paths) > 1:
            errors.append(f"重复 description: {', '.join(paths)}")

    if errors:
        print("搜索元数据审计失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"搜索元数据审计通过：{len(html_files)} 个 HTML，"
        f"{len(PRIORITY_PAGES)} 个 Bing 高优先级页面。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
