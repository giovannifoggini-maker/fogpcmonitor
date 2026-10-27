import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fogmonitor", ROOT / "FogMonitor.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CoreHelpersTests(unittest.TestCase):
    def test_fmt_bytes(self):
        self.assertEqual(MODULE.fmt_bytes(0), "0 B")
        self.assertEqual(MODULE.fmt_bytes(1024), "1.0 KB")
        self.assertEqual(MODULE.fmt_bytes(1024 ** 3), "1.0 GB")

    def test_resource_path_resolves_bundled_icon(self):
        icon = pathlib.Path(MODULE.resource_path("assets/fogmonitor-icon.png"))
        self.assertTrue(icon.is_file())

    def test_version_has_expected_release_format(self):
        self.assertRegex(MODULE.VERSION, r"^\d+\.\d+\.\d+$")

    def test_translation_catalogs_have_matching_keys(self):
        italian = set(MODULE.TRANSLATIONS["it"])
        english = set(MODULE.TRANSLATIONS["en"])
        self.assertEqual(italian, english)
        self.assertGreater(len(italian), 40)

    def test_language_settings_round_trip(self):
        from unittest.mock import patch
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            target = pathlib.Path(temp_dir) / "settings.json"
            with patch.object(MODULE, "settings_path", return_value=str(target)):
                MODULE.save_language_setting("en")
                self.assertEqual(MODULE.load_language_setting(), "en")
                MODULE.save_language_setting("it")
                self.assertEqual(MODULE.load_language_setting(), "it")



if __name__ == "__main__":
    unittest.main()
