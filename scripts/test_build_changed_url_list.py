from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_changed_url_list import ORIGIN, build_urls, route_for_file, sitemap_urls


class ChangedUrlListTests(unittest.TestCase):
    def test_all_uses_canonical_sitemap(self) -> None:
        urls = build_urls("", "HEAD", include_all=True)
        self.assertIn(f"{ORIGIN}/", urls)
        self.assertIn(f"{ORIGIN}/llms.txt", urls)
        self.assertIn(f"{ORIGIN}/sitemap.xml", urls)
        self.assertNotIn(f"{ORIGIN}/OPEN_SOURCE_BOUNDARY.md", urls)

    def test_internal_and_receipt_files_are_excluded(self) -> None:
        canonical = sitemap_urls()
        self.assertIsNone(route_for_file("scripts/submit_indexnow.py", canonical))
        self.assertIsNone(
            route_for_file(
                "docs/indexnow-submission-receipt-2026-08-16-reliability.json",
                canonical,
            )
        )

    def test_html_uses_canonical_route(self) -> None:
        canonical = sitemap_urls()
        self.assertEqual(route_for_file("index.html", canonical), f"{ORIGIN}/")


if __name__ == "__main__":
    unittest.main()
