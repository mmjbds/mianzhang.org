from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from submit_baidu import build_endpoint, load_urls, normalize_site


class SubmitBaiduTests(unittest.TestCase):
    def test_normalizes_origin(self) -> None:
        self.assertEqual(normalize_site("https://Example.com/"), "https://example.com")

    def test_loads_same_site_urls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "urls.txt"
            path.write_text(
                "https://example.com/\nhttps://example.com/research/\n",
                encoding="utf-8",
            )
            urls = load_urls(path, "https://example.com")
        self.assertEqual(len(urls), 2)

    def test_rejects_mixed_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "urls.txt"
            path.write_text("https://other.example/page\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside"):
                load_urls(path, "https://example.com")

    def test_rejects_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "urls.txt"
            path.write_text(
                "https://example.com/a\nhttps://example.com/a\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "duplicates"):
                load_urls(path, "https://example.com")

    def test_builds_encoded_endpoint(self) -> None:
        endpoint = build_endpoint(
            "http://data.zz.baidu.com/urls", "https://example.com", "secret-token"
        )
        parsed = urlsplit(endpoint)
        query = parse_qs(parsed.query)
        self.assertEqual(query["site"], ["https://example.com"])
        self.assertEqual(query["token"], ["secret-token"])


if __name__ == "__main__":
    unittest.main()
