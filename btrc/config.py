from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "Assets"
COLOR_CONFIG_PATH = BASE_DIR / "color_config.json"
TMP_DIR = BASE_DIR / "tmp"
OUTPUT_DIR = BASE_DIR / "Output"
EDITED_BRLYT_DIR = OUTPUT_DIR
EDITED_BRLAN_DIR = OUTPUT_DIR
BRLYT_JSON_DIR = TMP_DIR / "BRLYT"
BRLAN_JSON_DIR = TMP_DIR / "BRLAN"
WUJ5_DIR = BASE_DIR / "wuj5"
WUJ5_SCRIPT = WUJ5_DIR / "wuj5.py"
