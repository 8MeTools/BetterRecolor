# ButtonTextReColorizer ipynb 呼び出しセル最小構成

`ipynb` は呼び出しのみとし、実処理は `btrc/` 配下のモジュールを使う前提のセル構成例です。

---

## セル1: 設定と共通 import

```py
from btrc import BRLYT_JSON5_DIR, BRLAN_JSON5_DIR, WUJ5_SCRIPT, OUTPUT_DIR
from btrc.json5_io import list_json5_files, read_json5, write_json5
from btrc.brlyt import apply_tev_colors
from btrc.brlan import update_tev_colors, select_color_rule
from btrc.encode import encode_json5_files
from btrc.cleanup import remove_json5_files, move_all_files
from btrc.colors import run_color_input_flow, get_outline_color_from_user
```

---

## セル2: BRLYT 用カラー入力（プリセット反映まで）

```py
color_map = run_color_input_flow()
```

---

## セル3: テキスト縁取り色（BRLAN 用）

```py
default_free_text = (220, 220, 220)
default_select_text = (255, 255, 255)
free_outline = get_outline_color_from_user("free", "#282828")
select_outline = get_outline_color_from_user("select", "#787878")
text_free_colors = (default_free_text, free_outline)
text_select_colors = (default_select_text, select_outline)
```

---

## セル4: Assets → tmp へコピー（前処理）

```py
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
```

---

## セル5: BRLYT JSON5 を更新

```py
brlyt_files = list_json5_files(BRLYT_JSON5_DIR)
for path in brlyt_files:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text = apply_tev_colors(text, color_map)
    if new_text is not None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
```

---

## セル6: BRLAN JSON5 を更新

```py
brlan_files = list_json5_files(BRLAN_JSON5_DIR)
for path in brlan_files:
    data = read_json5(path)
    rule = select_color_rule(path, text_free_colors, text_select_colors)
    if rule is None:
        continue
    (start_outline, start_text), (end_outline, end_text) = rule
    updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
    write_json5(path, updated)
```

---

## セル7: JSON5 → BRLYT/BRLAN エンコード

```py
encode_json5_files(brlyt_files + brlan_files, WUJ5_SCRIPT)
```

---

## セル8: JSON5 削除

```py
remove_json5_files(brlyt_files + brlan_files)
```

---

## セル9: tmp → 完成フォルダへ移動

```py
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)
move_all_files(BRLYT_JSON5_DIR, OUTPUT_DIR)
move_all_files(BRLAN_JSON5_DIR, OUTPUT_DIR)
```
