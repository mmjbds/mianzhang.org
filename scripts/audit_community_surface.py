from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import yaml
except ImportError:  # pragma: no cover - explicit dependency message for clean environments
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SCAN_EXCLUSIONS = {
    Path("scripts/audit_community_surface.py"),
}
REQUIRED_FILES = {
    Path("LICENSE"),
    Path("OPEN_SOURCE_BOUNDARY.md"),
    Path("CONTENT_AND_MEDIA_LICENSE.md"),
    Path("COMMUNITY.md"),
    Path("GOVERNANCE.md"),
    Path("ROADMAP.md"),
    Path("community/index.html"),
    Path("zh/community/index.html"),
    Path(".github/CONTRIBUTING.md"),
    Path(".github/CODE_OF_CONDUCT.md"),
    Path(".github/SECURITY.md"),
    Path(".github/SUPPORT.md"),
    Path(".github/PULL_REQUEST_TEMPLATE.md"),
    Path(".github/ISSUE_TEMPLATE/public_artifact_improvement.yml"),
    Path(".github/DISCUSSION_TEMPLATE/q-and-a.yml"),
    Path(".github/DISCUSSION_TEMPLATE/research-and-extensions.yml"),
    Path(".github/DISCUSSION_TEMPLATE/ideas-and-use-cases.yml"),
    Path(".github/DISCUSSION_TEMPLATE/show-and-tell.yml"),
}
SECRET_PATTERNS = {
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
}
PRIVATE_PATH_PATTERNS = {
    "local project path": re.compile(r"[A-Za-z]:[\\/](?:Users|order-architect-factory)(?:[\\/]|\b)", re.I),
    "private core path": re.compile(r"\bsovereign_core[\\/]", re.I),
    "private forged-skill path": re.compile(r"\bskills[\\/]_forged(?:[\\/]|\b)", re.I),
    "tenant path": re.compile(r"\btenants[\\/]", re.I),
}
INTERNAL_LANGUAGE = {
    "仅供内部",
    "内部需要",
    "我们接下来要",
    "今日素材必须",
    "先回答外部读者",
    "for internal use only",
    "must first answer external readers",
}
PUBLIC_LANGUAGE_FILES = {
    Path("community/index.html"),
    Path("zh/community/index.html"),
    Path("COMMUNITY.md"),
    Path("GOVERNANCE.md"),
    Path("ROADMAP.md"),
}


class CommunityHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.canonical = ""
        self.hreflangs: dict[str, str] = {}
        self._in_json_ld = False
        self._json_parts: list[str] = []
        self.json_ld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag in {"a", "img", "link", "script"}:
            for key in ("href", "src"):
                if values.get(key):
                    self.links.append(values[key])
        if tag == "link":
            rel = values.get("rel", "").lower()
            if "canonical" in rel:
                self.canonical = values.get("href", "")
            if "alternate" in rel and values.get("hreflang"):
                self.hreflangs[values["hreflang"]] = values.get("href", "")
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld_blocks.append("".join(self._json_parts))
            self._in_json_ld = False


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root)
        if rel in SCAN_EXCLUSIONS:
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"LICENSE", "CNAME"}:
            files.append(path)
    return sorted(files)


def detect_sensitive_text(rel: Path, source: str) -> list[str]:
    errors: list[str] = []
    for label, pattern in {**SECRET_PATTERNS, **PRIVATE_PATH_PATTERNS}.items():
        if pattern.search(source):
            errors.append(f"{rel.as_posix()}: 检测到 {label}")
    return errors


def validate_required_files(root: Path) -> list[str]:
    return [f"缺少必需文件: {rel.as_posix()}" for rel in sorted(REQUIRED_FILES) if not (root / rel).is_file()]


def validate_license(root: Path) -> list[str]:
    path = root / "LICENSE"
    if not path.is_file():
        return []
    source = path.read_text(encoding="utf-8")
    required = {
        "Apache License": "Apache License",
        "Version 2.0": "Version 2.0, January 2004",
        "terms ending": "END OF TERMS AND CONDITIONS",
        "patent grant": "Grant of Patent License",
    }
    errors = [f"LICENSE: 缺少 Apache-2.0 {label}" for label, marker in required.items() if marker not in source]
    if len(source) < 11000:
        errors.append(f"LICENSE: 文件过短，疑似不是完整 Apache-2.0 文本 ({len(source)} bytes)")
    return errors


def resolve_local_link(page: Path, raw: str) -> Path | None:
    if raw.startswith(("http://", "https://", "mailto:", "data:", "#")):
        return None
    clean = unquote(raw.split("#", 1)[0].split("?", 1)[0])
    if not clean:
        return None
    target = (page.parent / clean).resolve()
    if target.is_dir():
        target /= "index.html"
    return target


def validate_community_pages(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    external_urls: list[str] = []
    expected = {
        Path("community/index.html"): {
            "canonical": "https://mianzhang.org/community/",
            "lang": "en",
        },
        Path("zh/community/index.html"): {
            "canonical": "https://mianzhang.org/zh/community/",
            "lang": "zh-Hans",
        },
    }
    required_routes = {
        "github.com/mmjbds/mianzhang.org/discussions",
        "huggingface.co/MMJBDS",
        "OPEN_SOURCE_BOUNDARY.md",
    }

    for rel, rules in expected.items():
        path = root / rel
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        parser = CommunityHTMLParser()
        parser.feed(source)
        if parser.canonical != rules["canonical"]:
            errors.append(f"{rel.as_posix()}: canonical 不正确")
        if f'<html lang="{rules["lang"]}">' not in source:
            errors.append(f"{rel.as_posix()}: html lang 不正确")
        for hreflang in ("en", "zh-Hans", "x-default"):
            if not parser.hreflangs.get(hreflang):
                errors.append(f"{rel.as_posix()}: 缺少 hreflang={hreflang}")
        if not parser.json_ld_blocks:
            errors.append(f"{rel.as_posix()}: 缺少 JSON-LD")
        for block in parser.json_ld_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel.as_posix()}: JSON-LD 无法解析: {exc}")
        for route in required_routes:
            if route not in source:
                errors.append(f"{rel.as_posix()}: 缺少公开路由 {route}")
        if "non-archival" not in source and "非存档" not in source:
            errors.append(f"{rel.as_posix()}: 缺少 KDD workshop 非存档边界")

        for raw in parser.links:
            target = resolve_local_link(path, raw)
            if target is not None:
                if not target.exists():
                    errors.append(f"{rel.as_posix()}: 本地链接不存在: {raw}")
            elif raw.startswith(("http://", "https://")):
                parsed = urlparse(raw)
                if not parsed.netloc:
                    errors.append(f"{rel.as_posix()}: 外部 URL 无效: {raw}")
                else:
                    external_urls.append(raw)
    return errors, sorted(set(external_urls))


def validate_yaml(root: Path) -> list[str]:
    if yaml is None:
        return ["缺少 PyYAML；请运行 pip install pyyaml"]
    errors: list[str] = []
    for path in sorted((root / ".github").rglob("*.yml")):
        rel = path.relative_to(root).as_posix()
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: YAML 无法解析: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: YAML 顶层必须是映射")
            continue
        if "DISCUSSION_TEMPLATE" in path.parts:
            body = data.get("body")
            if not isinstance(body, list) or not any(
                isinstance(item, dict) and item.get("type") != "markdown" for item in body
            ):
                errors.append(f"{rel}: discussion form 至少需要一个非 markdown 字段")
        if "ISSUE_TEMPLATE" in path.parts and path.name != "config.yml":
            if not data.get("name") or not isinstance(data.get("body"), list):
                errors.append(f"{rel}: issue form 缺少 name 或 body")
    return errors


def validate_indexes(root: Path) -> list[str]:
    errors: list[str] = []
    sitemap = root / "sitemap.xml"
    try:
        tree = ET.parse(sitemap)
        locations = {element.text for element in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
        for url in ("https://mianzhang.org/community/", "https://mianzhang.org/zh/community/"):
            if url not in locations:
                errors.append(f"sitemap.xml: 缺少 {url}")
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml: 无法解析: {exc}")

    llms_path = root / "llms.txt"
    llms = llms_path.read_text(encoding="utf-8") if llms_path.is_file() else ""
    for marker in (
        "https://mianzhang.org/community/",
        "https://mianzhang.org/zh/community/",
        "Open research community facts:",
        "Open-source boundary:",
    ):
        if marker not in llms:
            errors.append(f"llms.txt: 缺少 {marker}")
    return errors


def check_external_urls(urls: list[str]) -> list[str]:
    errors: list[str] = []
    headers = {"User-Agent": "mianzhang.org-community-audit/1.0"}
    for url in urls:
        request = urllib.request.Request(url, headers=headers, method="HEAD")
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                if response.status >= 400:
                    errors.append(f"外部链接返回 HTTP {response.status}: {url}")
        except urllib.error.HTTPError as exc:
            errors.append(f"外部链接返回 HTTP {exc.code}: {url}")
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"外部链接无法连接: {url} ({exc})")
    return errors


def run_audit(root: Path, check_external: bool = False) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_required_files(root))
    errors.extend(validate_license(root))
    page_errors, external_urls = validate_community_pages(root)
    errors.extend(page_errors)
    errors.extend(validate_yaml(root))
    errors.extend(validate_indexes(root))

    for path in iter_text_files(root):
        rel = path.relative_to(root)
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        errors.extend(detect_sensitive_text(rel, source))
        if rel in PUBLIC_LANGUAGE_FILES:
            folded = source.casefold()
            for phrase in INTERNAL_LANGUAGE:
                if phrase.casefold() in folded:
                    errors.append(f"{rel.as_posix()}: 检测到内部口吻: {phrase}")

    if check_external:
        errors.extend(check_external_urls(external_urls))
    return sorted(set(errors))


def run_self_test() -> list[str]:
    failures: list[str] = []
    secret = "hf_" + "A" * 24
    if not detect_sensitive_text(Path("fixture.md"), secret):
        failures.append("自测失败: 未识别动态令牌夹具")
    private_path = "C:" + "\\Users\\Administrator\\private.txt"
    if not detect_sensitive_text(Path("fixture.md"), private_path):
        failures.append("自测失败: 未识别本机路径夹具")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "LICENSE").write_text("Apache License", encoding="utf-8")
        if not validate_license(root):
            failures.append("自测失败: 未识别缩短许可证")

        page = root / "community" / "index.html"
        page.parent.mkdir(parents=True)
        page.write_text('<a href="missing.html">missing</a>', encoding="utf-8")
        parser = CommunityHTMLParser()
        parser.feed(page.read_text(encoding="utf-8"))
        target = resolve_local_link(page, parser.links[0])
        if target is None or target.exists():
            failures.append("自测失败: 未构造断裂本地链接")

        if yaml is not None:
            bad_yaml = root / ".github" / "DISCUSSION_TEMPLATE" / "q-and-a.yml"
            bad_yaml.parent.mkdir(parents=True)
            bad_yaml.write_text("body: [", encoding="utf-8")
            if not validate_yaml(root):
                failures.append("自测失败: 未识别损坏 YAML")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="审计公开社区、许可、敏感边界和路由。")
    parser.add_argument("--check-external", action="store_true", help="同时检查社区页外部 HTTP 链接")
    parser.add_argument("--self-test", action="store_true", help="先运行失败夹具自测")
    args = parser.parse_args()

    errors: list[str] = []
    if args.self_test:
        errors.extend(run_self_test())
    errors.extend(run_audit(ROOT, check_external=args.check_external))

    if errors:
        print("社区公开面审计失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print("社区公开面审计通过：许可、边界、YAML、路由、索引与敏感信息检查均正常。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
