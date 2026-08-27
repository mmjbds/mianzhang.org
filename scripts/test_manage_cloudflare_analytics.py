from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import manage_cloudflare_analytics as analytics


class CloudflareAnalyticsTests(unittest.TestCase):
    def test_inject_is_idempotent_and_auditable(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text("<html><body><p>Page</p></body></html>", encoding="utf-8")

            self.assertTrue(analytics.inject(path))
            self.assertFalse(analytics.inject(path))
            self.assertEqual(analytics.audit_file(path), [])
            source = path.read_text(encoding="utf-8")
            self.assertEqual(source.count(analytics.BEACON_URL), 1)
            self.assertLess(source.index(analytics.SNIPPET), source.index("</body>"))

    def test_noncanonical_existing_beacon_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(
                f"<html><body><script src='{analytics.BEACON_URL}'></script></body></html>",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                analytics.inject(path)

    def test_verification_file_without_body_is_not_eligible(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "verify.html").write_text("verification-token", encoding="utf-8")
            self.assertEqual(analytics.eligible_html(root), [])


if __name__ == "__main__":
    unittest.main()
