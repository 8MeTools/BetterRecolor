# ButtonTextReColorizer モジュール分割フロー（案）

本書は `docs/BTRC-Before.md` を前提に、`ipynb` を最小化し、処理を `.py` モジュールとして分割するための実装フローをまとめたものです。  
今回は「関数化・モジュール分割の設計のみ」を目的とし、文字列変換処理の効率化は行いません。

---

## 1. 目的と前提

- `ipynb` は呼び出しと結果表示だけにして、実処理は `.py` に移す
- ローカル/Colab/別PCでパスを差し替えられるようにする
- 将来的な `i18n`（多言語対応）を想定した構成にする

---

## 2. 推奨フォルダ構成（例）

```
ButtonTextReColorizer/
  btrc/
    __init__.py
    config.py
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
  ButtonTextReColorizer.ipynb
```

---

## 3. configでパスを管理する理由と方針

### 理由

- ローカル/Colab/別PCの「環境差分」を分離できる
- パス変更が `config` の差し替えだけで済む
- 本体コードがパス依存から解放され、再利用・テストがしやすい

### 方針

- `config.py` にベースパスと派生パスを集約する
- できれば `config_local.py` で上書きできるようにしておく  
  （環境ごとの差分だけを局所化できる）

---

## 4. configの最小例（設計イメージ）

```py
# btrc/config.py
from pathlib import Path

# 環境差分の起点
BASE_DIR = Path(".").resolve()

# 主要ディレクトリ
ASSETS_DIR = BASE_DIR / "Assets"
TMP_DIR = BASE_DIR / "tmp"
EDITED_BRLYT_DIR = BASE_DIR / "EditedBRLYT"
EDITED_BRLAN_DIR = BASE_DIR / "EditedBRLAN"

# JSON5作業ディレクトリ
BRLYT_JSON5_DIR = TMP_DIR / "BRLYT"
BRLAN_JSON5_DIR = TMP_DIR / "BRLAN"

# wuj5.py の位置（ローカル配置想定）
WUJ5_DIR = BASE_DIR / "wuj5"
WUJ5_SCRIPT = WUJ5_DIR / "wuj5.py"
```

```py
# btrc/config_local.py（任意）
from pathlib import Path
from .config import *

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
# btrc/__init__.py で上書きを読むイメージ
try:
    from .config_local import *  # noqa
except Exception:
    from .config import *  # noqa
```

---

## 5. モジュール分割の流れ

### (1) 共有処理の抽出

- `json5_io.py`
  - JSON5ファイル探索（`os.walk` の重複削除）
  - JSON5の読み書きの入口
- `encode.py`
  - `wuj5.py encode` の実行
  - BRLYT/BRLANで共通化
- `cleanup.py`
  - JSON5の削除
  - 完成フォルダへの移動

### (2) カラー入力の分離

- `colors.py`
  - `get_valid_hex_color`
  - `get_outline_color_from_user`
  - プリセット定義
  - プレビュー表示

### (3) BRLYT / BRLAN 固有処理の分離

- `brlyt.py`
  - JSON5文字列の置換処理（正規表現ベース）
  - 置換に使う `color_map` の責務を集約
- `brlan.py`
  - `update_tev_colors` を移動
  - ファイル名ルールを関数化  
    （後でテーブル化しやすい）

---

## 6. ipynbの最小化（実行順だけ残す）

1. `colors.py` でカラー入力と確認  
2. `json5_io.py` で対象JSON5を列挙  
3. `brlyt.py` / `brlan.py` で更新  
4. `encode.py` でエンコード  
5. `cleanup.py` で削除・移動  

Notebook側は「実行順」を示すだけにし、ロジックは `.py` に閉じ込める。

---

## 7. i18n対応の下準備

- `i18n.py` で表示文言を辞書化
  - `MESSAGES["ja"]["invalid_hex"]` のように定義
- `colors.py` などの `print()` は `i18n.get("invalid_hex")` を参照  
  （将来は `LANG` の切り替えで多言語化可能）

---

## 8. このフローで得られる効果

- `ipynb` が読みやすく、変更箇所が明確になる
- ローカル環境でも動かしやすくなる
- Gitでの差分確認がしやすい
- i18nや将来拡張に強くなる

