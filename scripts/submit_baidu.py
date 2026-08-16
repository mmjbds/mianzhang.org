from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_ENDPOINT = "http://data.zz.baidu.com/urls"


def normalize_site(site: str) -> str:
    parsed = urllib.parse.urlsplit(site.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Site must be an absolute HTTP(S) origin")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("Site must not contain a path, query, or fragment")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc.lower(), "", "", ""))


def load_urls(path: Path, site: str) -> list[str]:
    urls = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    urls = [url for url in urls if url and not url.startswith("#")]
    if not urls:
        raise ValueError("URL list is empty")
    if len(set(urls)) != len(urls):
        raise ValueError("URL list contains duplicates")

    site_origin = normalize_site(site)
    site_host = urllib.parse.urlsplit(site_origin).netloc
    for url in urls:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")
        if parsed.netloc.lower() != site_host:
            raise ValueError(f"URL is outside the submitted site: {url}")
        if parsed.fragment:
            raise ValueError(f"URL must not contain a fragment: {url}")
    return urls


def build_endpoint(endpoint: str, site: str, token: str) -> str:
    token = token.strip()
    if not token or any(char.isspace() for char in token):
        raise ValueError("Baidu token must be one non-empty token")
    query = urllib.parse.urlencode({"site": normalize_site(site), "token": token})
    return f"{endpoint}?{query}"


def submit(urls: list[str], endpoint: str, timeout: int) -> tuple[int, dict[str, object]]:
    request = urllib.request.Request(
        endpoint,
        data="\n".join(urls).encode("utf-8"),
        headers={"Content-Type": "text/plain; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"message": body}
        return exc.code, payload


def write_receipt(
    path: Path,
    site: str,
    url_list: Path,
    url_count: int,
    status_code: int,
    response: dict[str, object],
) -> None:
    now = datetime.now(timezone.utc)
    accepted = status_code == 200 and "error" not in response
    receipt = {
        "receipt_id": f"baidu-{now:%Y%m%dT%H%M%SZ}",
        "provider": "Baidu Search Resource Platform",
        "submitted_at_utc": now.isoformat(),
        "submitted_at_asia_shanghai": now.astimezone(
            ZoneInfo("Asia/Shanghai")
        ).isoformat(),
        "request": {
            "site": normalize_site(site),
            "url_count": url_count,
            "url_list_source": url_list.as_posix(),
            "token_source": "environment variable (value not recorded)",
        },
        "response": {
            "status_code": status_code,
            "accepted": accepted,
            "body": response,
        },
        "boundary": (
            "API acceptance only records that Baidu received the submitted URLs. "
            "It does not prove crawling, indexing, ranking, traffic, or AI retrieval."
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit a URL list to Baidu")
    parser.add_argument("--url-list", type=Path, required=True)
    parser.add_argument("--site", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--token-env", default="BAIDU_PUSH_TOKEN")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        site = normalize_site(args.site)
        urls = load_urls(args.url_list, site)
        if args.dry_run:
            print(json.dumps({"site": site, "url_count": len(urls)}, indent=2))
            return 0
        token = os.environ.get(args.token_env, "")
        endpoint = build_endpoint(args.endpoint, site, token)
    except (OSError, ValueError) as exc:
        print(f"Baidu submission input error: {exc}", file=sys.stderr)
        return 2

    status_code, response = submit(urls, endpoint, args.timeout)
    write_receipt(args.receipt, site, args.url_list, len(urls), status_code, response)
    redacted = {
        "status_code": status_code,
        "url_count": len(urls),
        "response": response,
        "receipt": args.receipt.as_posix(),
    }
    print(json.dumps(redacted, ensure_ascii=True))
    return 0 if status_code == 200 and "error" not in response else 1


if __name__ == "__main__":
    raise SystemExit(main())
