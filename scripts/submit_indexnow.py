from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENDPOINT = "https://api.indexnow.org/indexnow"


def load_urls(path: Path) -> list[str]:
    urls = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    urls = [url for url in urls if url and not url.startswith("#")]
    if not urls:
        raise ValueError("URL list is empty")
    if len(urls) > 10_000:
        raise ValueError("IndexNow accepts at most 10,000 URLs per POST")
    if len(set(urls)) != len(urls):
        raise ValueError("URL list contains duplicates")
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")
    return urls


def build_payload(urls: list[str], key_file: Path) -> dict[str, object]:
    hosts = {urlparse(url).netloc.lower() for url in urls}
    if len(hosts) != 1:
        raise ValueError("Submit one host per IndexNow request")
    host = hosts.pop()
    key = key_file.read_text(encoding="utf-8").strip()
    if not 8 <= len(key) <= 128 or any(char.isspace() for char in key):
        raise ValueError("IndexNow key must be a single 8-128 character token")
    return {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key_file.name}",
        "urlList": urls,
    }


def submit(payload: dict[str, object], endpoint: str, timeout: int) -> int:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code


def write_receipt(
    path: Path,
    payload: dict[str, object],
    url_list: Path,
    status_code: int,
) -> None:
    now = datetime.now(timezone.utc)
    public_payload = {key: value for key, value in payload.items() if key != "key"}
    receipt = {
        "receipt_id": f"indexnow-{now:%Y%m%dT%H%M%SZ}",
        "provider": "IndexNow",
        "submitted_at_utc": now.isoformat(),
        "submitted_at_asia_shanghai": now.astimezone(ZoneInfo("Asia/Shanghai")).isoformat(),
        "request": {
            **public_payload,
            "url_count": len(payload["urlList"]),
            "url_list_source": url_list.as_posix(),
        },
        "response": {"status_code": status_code, "accepted": status_code in {200, 202}},
        "boundary": (
            "HTTP 200 or 202 records IndexNow request acceptance only. "
            "It does not prove crawling, indexing, ranking, backlink attribution, or AI retrieval."
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit a host-specific URL list to IndexNow")
    parser.add_argument("--url-list", type=Path, required=True)
    parser.add_argument("--key-file", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        urls = load_urls(args.url_list)
        payload = build_payload(urls, args.key_file)
    except (OSError, ValueError) as exc:
        print(f"IndexNow input error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        redacted = {key: value for key, value in payload.items() if key != "key"}
        redacted["url_count"] = len(urls)
        print(json.dumps(redacted, ensure_ascii=True, indent=2))
        return 0

    status_code = submit(payload, args.endpoint, args.timeout)
    write_receipt(args.receipt, payload, args.url_list, status_code)
    print(f"IndexNow response: HTTP {status_code}; receipt: {args.receipt}")
    return 0 if status_code in {200, 202} else 1


if __name__ == "__main__":
    raise SystemExit(main())
