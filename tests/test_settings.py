import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from holidaysnek import settings
class SettingsTests(unittest.TestCase):
    def test_defaults(self):
        with patch.object(settings, "config_path", return_value=Path("/definitely/missing/config.json")):
            result = settings.load_settings()
        self.assertEqual(result["scene"], "halloween"); self.assertEqual(result["speed"], 1.0)
    def test_clamps_bad_values(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.json"; path.write_text(json.dumps({"scene": "x", "speed": 99, "intensity": -5}))
            with patch.object(settings, "config_path", return_value=path): result = settings.load_settings()
        self.assertEqual(result["speed"], 3.0); self.assertEqual(result["intensity"], .1)
if __name__ == "__main__": unittest.main()
