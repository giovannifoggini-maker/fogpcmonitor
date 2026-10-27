from pathlib import Path
import tomllib
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class CloudflarePagesPackageTests(unittest.TestCase):
    def test_pages_output_has_entrypoint_and_assets(self):
        self.assertTrue((PUBLIC / "index.html").is_file())
        self.assertTrue((PUBLIC / "styles.css").is_file())
        self.assertTrue((PUBLIC / "app.js").is_file())
        self.assertTrue((PUBLIC / "404.html").is_file())
        self.assertTrue((PUBLIC / "_headers").is_file())

    def test_download_link_points_to_existing_source_zip(self):
        index = (PUBLIC / "index.html").read_text(encoding="utf-8")
        relative = "downloads/FogMonitor-by-FogLabs-v1.7.0-IT-EN.zip"
        self.assertIn('/' + relative, index)
        self.assertTrue((PUBLIC / relative).is_file())
        with zipfile.ZipFile(PUBLIC / relative) as archive:
            self.assertIn("FogMonitor-FogLabs/FogMonitor.py", archive.namelist())
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in archive.namelist()))

    def test_wrangler_pages_output_directory(self):
        config = tomllib.loads((ROOT / "wrangler.toml").read_text(encoding="utf-8"))
        self.assertEqual(config.get("pages_build_output_dir"), "./public")
        self.assertTrue((ROOT / config["pages_build_output_dir"] / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
