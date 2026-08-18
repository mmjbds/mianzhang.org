from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from submit_indexnow import build_payload, load_urls


class SubmitIndexNowTests(unittest.TestCase):
    def test_builds_host_specific_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            url_list = root / "urls.txt"
            key_file = root / "abc12345.txt"
            url_list.write_text("https://example.com/a\nhttps://example.com/b\n", encoding="utf-8")
            key_file.write_text("abc12345\n", encoding="utf-8")
            payload = build_payload(load_urls(url_list), key_file)
        self.assertEqual(payload["host"], "example.com")
        self.assertEqual(payload["keyLocation"], "https://example.com/abc12345.txt")
        self.assertEqual(len(payload["urlList"]), 2)

    def test_rejects_mixed_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            url_list = root / "urls.txt"
            key_file = root / "abc12345.txt"
            url_list.write_text("https://example.com/a\nhttps://other.example/b\n", encoding="utf-8")
            key_file.write_text("abc12345\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "one host"):
                build_payload(load_urls(url_list), key_file)

    def test_rejects_duplicate_urls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "urls.txt"
            path.write_text("https://example.com/a\nhttps://example.com/a\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicates"):
                load_urls(path)


if __name__ == "__main__":
    unittest.main()
