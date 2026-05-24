# ButtonTextReColorizer モジュール分割フロー（コード付き）

本書は `docs/BTRC-Before.md` を前提に、`ipynb` を最小化し、処理を `.py` モジュールとして分割するための「具体的なPythonコード例」を含む手順書です。  
文字列変換処理の効率化は行わず、構造の整理（関数化・モジュール化）に集中します。

---

## 1. 前提とゴール

- `ipynb` は呼び出しのみ
- 実処理は `btrc/` 配下に移動
- パスは `config` で一元管理
- i18nを見据えたメッセージ管理を導入

---

## 2. 推奨フォルダ構成

```
ButtonTextReColorizer/
  btrc/
    __init__.py
    config.py
    config_local.py      (任意)
    i18n.py
    colors.py
    json5_io.py
    brlyt.py
    brlan.py
    encode.py
    cleanup.py
  docs/
    BTRC-Before.md
    Refactor-Flow.md
    Refactor-Flow-With-Code.md
  ButtonTextReColorizer.ipynb
```

---

## 3. configでパスを管理する

```py
# btrc/config.py
from pathlib import Path

BASE_DIR = Path(".").resolve()
ASSETS_DIR = BASE_DIR / "Assets"
TMP_DIR = BASE_DIR / "tmp"
EDITED_BRLYT_DIR = BASE_DIR / "EditedBRLYT"
EDITED_BRLAN_DIR = BASE_DIR / "EditedBRLAN"
BRLYT_JSON5_DIR = TMP_DIR / "BRLYT"
BRLAN_JSON5_DIR = TMP_DIR / "BRLAN"
WUJ5_DIR = BASE_DIR / "wuj5"
WUJ5_SCRIPT = WUJ5_DIR / "wuj5.py"
```

```py
# btrc/config_local.py（任意）
from pathlib import Path
from .config import *  # noqa

BASE_DIR = Path("D:/Games/MKW/Mods/2026/ButtonTextReColorizer")
ASSETS_DIR = BASE_DIR / "Assets"
TMP_DIR = BASE_DIR / "tmp"
EDITED_BRLYT_DIR = BASE_DIR / "EditedBRLYT"
EDITED_BRLAN_DIR = BASE_DIR / "EditedBRLAN"
BRLYT_JSON5_DIR = TMP_DIR / "BRLYT"
BRLAN_JSON5_DIR = TMP_DIR / "BRLAN"
WUJ5_DIR = BASE_DIR / "wuj5"
WUJ5_SCRIPT = WUJ5_DIR / "wuj5.py"
```

```py
# btrc/__init__.py
try:
    from .config_local import *  # noqa
except Exception:
    from .config import *  # noqa
```

---

## 4. i18nの土台

```py
# btrc/i18n.py
MESSAGES = {
    "ja": {
        "invalid_hex": "無効なカラーコードです。#RRGGBB の形式で入力してください。",
        "no_json5": "指定されたディレクトリにJSON5ファイルが存在しません。",
        "done_encode": "すべてのJSON5ファイルをエンコードしました！",
    },
    "en": {
        "invalid_hex": "Invalid color code. Use #RRGGBB.",
        "no_json5": "No JSON5 files found in the directory.",
        "done_encode": "All JSON5 files were encoded!",
    },
}

LANG = "ja"

def t(key):
    return MESSAGES.get(LANG, {}).get(key, key)
```

---

## 5. JSON5共通処理

```py
# btrc/json5_io.py
import os
import json5

def list_json5_files(root_dir):
    json5_files = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".json5"):
                json5_files.append(os.path.join(root, f))
    return json5_files

def read_json5(path):
    with open(path, "r", encoding="utf-8") as f:
        return json5.load(f)

def write_json5(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json5.dump(data, f, indent=2)
```

---

## 6. カラー入力の整理

```py
# btrc/colors.py
import re
from colr import color
from .i18n import t

HEX_PATTERN = re.compile(r"^#([A-Fa-f0-9]{6})$")

def get_valid_hex_color(prompt):
    while True:
        value = input(prompt).strip()
        if HEX_PATTERN.match(value):
            return value
        print(t("invalid_hex"))

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return "#%02X%02X%02X" % (r, g, b)

def print_color(name, rgb):
    print(f"{name}: {rgb} {color('■', fore=rgb_to_hex(*rgb))}")

def get_outline_color_from_user(state_name, default_hex):
    while True:
        user_input = input(
            f"{state_name} の縁取りカラー（空欄でデフォルト {default_hex}）: "
        ).strip()
        if user_input == "":
            user_input = default_hex
        if HEX_PATTERN.match(user_input):
            return tuple(int(user_input[i:i+2], 16) for i in (1, 3, 5))
        print(t("invalid_hex"))
```

---

## 7. カラー入力→プリセット反映までの例

```py
# btrc/colors.py（追記例）

# カラープリセット（初期値）
color_presets = {
    "fuchi_pattern2": {"black": "#ffffff", "white": "#000000"},
    "color_base2": {"black": "#434343", "white": "#434343"},
    "black_base2": {"black": "#434343", "white": "#434343"},
    "pikapika": {"black": "#ffffff", "white": "#ffffff"},
    "color_yajirushi": {"black": "#FFFFFF", "white": "#C8C8C8"},
    "ability_graph2": {"black": "#434343", "white": "#434343"},
    "black_pt00": {"black": "#434343", "white": "#434343"},
    "black_pt01": {"black": "#434343", "white": "#434343"},
}

def print_preset(name):
    preset = color_presets[name]
    print(f"◆{name} のカラー◆")
    print(f"BlackColor: {preset['black']} {color('■', fore=preset['black'])}")
    print(f"WhiteColor: {preset['white']} {color('■', fore=preset['white'])}")

def get_custom_color_and_update(name):
    print(f"\n=== {name} のカラー設定 ===")
    default_black = color_presets[name]["black"]
    default_white = color_presets[name]["white"]
    print(f"デフォルト → Black: {default_black}, White: {default_white}")

    # ここでは常にユーザー入力する前提（既存コードに合わせる）
    black = get_valid_hex_color(f"{name}のBlackColorを入力してください: ")
    white = get_valid_hex_color(f"{name}のWhiteColorを入力してください: ")

    # プリセットを更新
    color_presets[name]["black"] = black
    color_presets[name]["white"] = white

    # 一部のpane名は連動して更新
    if name == "color_base2":
        color_presets["black_base2"]["black"] = black
        color_presets["black_base2"]["white"] = white
        color_presets["pikapika"]["black"] = black
        color_presets["pikapika"]["white"] = white
    elif name == "ability_graph2":
        color_presets["black_pt00"]["black"] = black
        color_presets["black_pt00"]["white"] = white
        color_presets["black_pt01"]["black"] = black
        color_presets["black_pt01"]["white"] = white

    return hex_to_rgb(black), hex_to_rgb(white)

def run_color_input_flow():
    fuchi_black_rgb, fuchi_white_rgb = get_custom_color_and_update("fuchi_pattern2")
    base_black_rgb, base_white_rgb = get_custom_color_and_update("color_base2")
    arrow_black_rgb, arrow_white_rgb = get_custom_color_and_update("color_yajirushi")
    ability_black_rgb, ability_white_rgb = get_custom_color_and_update("ability_graph2")

    print("\n=== カラープレビュー ===")
    for preset_name in color_presets:
        print_preset(preset_name)

    # BRLYTのcolor_map用にまとめて返す
    color_map = {
        "fuchi_pattern2": (fuchi_black_rgb, fuchi_white_rgb),
        "color_base2": (base_black_rgb, base_white_rgb),
        "black_base2": (base_black_rgb, base_white_rgb),
        "pikapika": (base_black_rgb, base_white_rgb),
        "color_yajirushi": (arrow_black_rgb, arrow_white_rgb),
        "ability_graph2": (ability_black_rgb, ability_white_rgb),
        "black_pt00": (ability_black_rgb, ability_white_rgb),
        "black_pt01": (ability_black_rgb, ability_white_rgb),
    }
    return color_map
```

---

## 8. BRLYT用の処理分離

```py
# btrc/brlyt.py
import re

def apply_tev_colors(json_text, color_map):
    pattern = re.compile(
        r'(\\s*"name": "(fuchi_pattern2|color_base2|black_base2|pikapika|'
        r'color_yajirushi|ability_graph2|black_pt00|black_pt01|text|active_text|chara02)"'
        r'.*?("tev color 1 a": \\d+))',
        re.DOTALL
    )
    matches = list(re.finditer(pattern, json_text))
    if not matches:
        return None

    for match in reversed(matches):
        block_text = match.group(1)
        block_name = match.group(2)
        black_rgb, white_rgb = color_map.get(block_name, ((0, 0, 0), (255, 255, 255)))

        block_text = re.sub(r'"tev color 0 r": \\d+(,?)', f'"tev color 0 r": {black_rgb[0]}\\1', block_text)
        block_text = re.sub(r'"tev color 0 g": \\d+(,?)', f'"tev color 0 g": {black_rgb[1]}\\1', block_text)
        block_text = re.sub(r'"tev color 0 b": \\d+(,?)', f'"tev color 0 b": {black_rgb[2]}\\1', block_text)

        block_text = re.sub(r'"tev color 1 r": \\d+(,?)', f'"tev color 1 r": {white_rgb[0]}\\1', block_text)
        block_text = re.sub(r'"tev color 1 g": \\d+(,?)', f'"tev color 1 g": {white_rgb[1]}\\1', block_text)
        block_text = re.sub(r'"tev color 1 b": \\d+(,?)', f'"tev color 1 b": {white_rgb[2]}\\1', block_text)

        json_text = json_text[:match.start()] + block_text + json_text[match.end():]

    return json_text
```

---

## 9. BRLAN用の処理分離

```py
# btrc/brlan.py
def update_tev_colors(data, start_outline, start_text, end_outline, end_text):
    for section in data.get("sections", []):
        for content in section.get("contents", []):
            if content.get("name") != "text":
                continue
            for animation in content.get("animations", []):
                for target in animation.get("targets", []):
                    kind = target.get("kind", "")
                    if not kind.startswith("tev color"):
                        continue
                    color_type = kind.split()[2]
                    component = kind.split()[-1]

                    for key in target.get("keys", []):
                        if start_outline == end_outline and start_text == end_text:
                            color = start_text if color_type == "0" else start_outline
                        else:
                            color = (
                                start_text if (color_type == "0" and key["frame"] == 0.0)
                                else end_text if (color_type == "0")
                                else start_outline if (color_type == "1" and key["frame"] == 0.0)
                                else end_outline
                            )
                        if component == "r":
                            key["value"] = color[0]
                        elif component == "g":
                            key["value"] = color[1]
                        elif component == "b":
                            key["value"] = color[2]
    return data

def select_color_rule(filename, text_free_colors, text_select_colors):
    name = filename.lower()
    if "free_to_select" in name:
        return text_free_colors, text_select_colors
    if "select_to_free" in name:
        return text_select_colors, text_free_colors
    if "free" in name and "select" not in name:
        return (text_free_colors, text_free_colors)
    if "select" in name and "free" not in name:
        return (text_select_colors, text_select_colors)
    if "stop" in name:
        return (text_select_colors, text_select_colors)
    if "common_w098_wifi_menu_text" in name:
        return (text_select_colors, text_select_colors)
    if "common_w010_cup_fuchi_off" in name or "common_w010_cup_fuchi_on_to_off" in name:
        return (text_select_colors, text_select_colors)
    if "fuchi_check_loop" in name:
        return None
    return None
```

---

## 10. JSON5 → BRLYT/BRLAN 変換

```py
# btrc/encode.py
import subprocess
from .i18n import t

def encode_json5_files(files, wuj5_script):
    if not files:
        print(t("no_json5"))
        return
    for file_path in files:
        command = ["python", str(wuj5_script), "encode", file_path]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"エラー: {file_path}")
            print(e.stderr)
    print(t("done_encode"))
```

---

## 11. JSON5削除・移動処理

```py
# btrc/cleanup.py
import os
import shutil

def remove_json5_files(files):
    for path in files:
        os.remove(path)

def move_all_files(src_dir, dst_dir):
    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        shutil.move(src, dst)
```

---

## 12. ipynb側の最小構成（具体セル案）

```py
# セル1: 設定と共通import
from btrc import BRLYT_JSON5_DIR, BRLAN_JSON5_DIR, WUJ5_SCRIPT
from btrc.json5_io import list_json5_files, read_json5, write_json5
from btrc.brlyt import apply_tev_colors
from btrc.brlan import update_tev_colors, select_color_rule
from btrc.encode import encode_json5_files
from btrc.cleanup import remove_json5_files, move_all_files
from btrc.colors import run_color_input_flow, get_outline_color_from_user

# セル2: BRLYT 用カラー入力（プリセット反映まで）
color_map = run_color_input_flow()

# セル3: テキスト縁取り色（BRLAN 用）
default_free_text = (220, 220, 220)
default_select_text = (255, 255, 255)
free_outline = get_outline_color_from_user("free", "#282828")
select_outline = get_outline_color_from_user("select", "#787878")
text_free_colors = (default_free_text, free_outline)
text_select_colors = (default_select_text, select_outline)

# セル4: Assets → tmp へコピー（前処理）
import os
import shutil

os.makedirs(BRLYT_JSON5_DIR, exist_ok=True)
os.makedirs(BRLAN_JSON5_DIR, exist_ok=True)

def copy_all(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        os.makedirs(dst_root, exist_ok=True)
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(dst_root, f)
            shutil.copy2(src, dst)

copy_all(str(BRLYT_JSON5_DIR).replace("tmp/BRLYT", "Assets/BRLYT"), str(BRLYT_JSON5_DIR))
copy_all(str(BRLAN_JSON5_DIR).replace("tmp/BRLAN", "Assets/BRLAN"), str(BRLAN_JSON5_DIR))

# セル5: BRLYT JSON5 を更新
brlyt_files = list_json5_files(BRLYT_JSON5_DIR)
for path in brlyt_files:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text = apply_tev_colors(text, color_map)
    if new_text is not None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)

# セル6: BRLAN JSON5 を更新
brlan_files = list_json5_files(BRLAN_JSON5_DIR)
for path in brlan_files:
    data = read_json5(path)
    rule = select_color_rule(path, text_free_colors, text_select_colors)
    if rule is None:
        continue
    (start_outline, start_text), (end_outline, end_text) = rule
    updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
    write_json5(path, updated)

# セル7: JSON5 → BRLYT/BRLAN エンコード
encode_json5_files(brlyt_files + brlan_files, WUJ5_SCRIPT)

# セル8: JSON5 削除
remove_json5_files(brlyt_files + brlan_files)

# セル9: tmp → 完成フォルダへ移動
import os
os.makedirs(EDITED_BRLYT_DIR, exist_ok=True)
os.makedirs(EDITED_BRLAN_DIR, exist_ok=True)
move_all_files(BRLYT_JSON5_DIR, EDITED_BRLYT_DIR)
move_all_files(BRLAN_JSON5_DIR, EDITED_BRLAN_DIR)
```

---

## 13. 補足

- `color_map` / `text_free_colors` などは `colors.py` で生成し、Notebook側は受け取るだけにする
- `config_local.py` を用意すると、ローカル専用パスに差し替えやすい
