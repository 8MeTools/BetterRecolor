## 環境の準備

- Googleドライブのマウント(colab専用)

```py
# Googleドライブのマウント
from google.colab import drive
drive.mount('/content/drive')
```

```sh
# Googleドライブのマイドライブへ移動.
%cd /content/drive/MyDrive
#マイドライブ直下に8MeToolsフォルダを生成.
!mkdir -p ./8MeTools/BTRC
#8MeToolsフォルダに移動
%cd /content/drive/MyDrive/8MeTools
#8MeToolsフォルダ内に必要ファイルをダウンロード.
!git clone https://github.com/8MeTools/ButtonTextReColorizer.git
#フォルダ名のリネーム.
!mv "/content/drive/MyDrive/8MeTools/ButtonTextReColorizer/"* "/content/drive/MyDrive/8MeTools/BTRC/"
#不要データの削除(GitHub上では必要ですが、作業においては必要のないものです)
!rm -r "/content/drive/MyDrive/8MeTools/ButtonTextReColorizer/"
!rm /content/drive/MyDrive/8MeTools/BTRC/EditedBRLAN/.gitkeep
!rm /content/drive/MyDrive/8MeTools/BTRC/EditedBRLYT/.gitkeep
!rm /content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN/.gitkeep
!rm /content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT/.gitkeep
# ファイル,ディレクトリが存在しているかどうかを確認する
%ls /content/drive/MyDrive/8MeTools/BTRC -l

%cd /content
!git clone https://github.com/stblr/wuj5.git
!pip install colour colr
!pip install json5
%cd /content/wuj5
!ls -l

# これを実行したあと、"/content/wuj5"と出ていればOK
!pwd
```

## カラーコードの定義

```python
import re
from colr import color

# カラーコード判定関数
def get_valid_hex_color(prompt):
    """ ユーザーにカラーコードを入力させ、正しい形式 (#RRGGBB) でなければ再入力を求める """
    hex_pattern = re.compile(r"^#([A-Fa-f0-9]{6})$")

    while True:
        color = input(prompt).strip()
        if hex_pattern.match(color):
            return color
        else:
            print("無効なカラーコードです。#RRGGBB の形式で入力してください。")

# HTMLカラーコードをRGBに変換する関数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# カラープリセット（デフォルト値）
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

# ユーザーにカラー設定をさせてプリセットを更新する関数
def get_custom_color_and_update(name):
    print(f"\n=== {name} のカラー設定 ===")

    # 既存のプリセットからデフォルト値を取得
    default_black = color_presets[name]["black"]
    default_white = color_presets[name]["white"]
    print(f"デフォルト → Black: {default_black}, White: {default_white}")

    # use_default = input("デフォルトのままにしますか？（Y/n）: ").strip().lower()
    use_default = "n"
    if use_default == "n":
        black = get_valid_hex_color(f"{name}のBlackColorを入力してください: ")
        white = get_valid_hex_color(f"{name}のWhiteColorを入力してください: ")

        # ここで元の辞書を更新
        color_presets[name]["black"] = black
        color_presets[name]["white"] = white

        # 一部のpane名の場合は、類似するpaneに対しても反映を適用させる
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


# 指定されたプリセット名の色情報を表示する関数
def print_colors(preset_name):
    if preset_name in color_presets:
        preset = color_presets[preset_name]
        black_color = preset["black"]
        white_color = preset["white"]

        print(f"◆{preset_name} のカラー◆")
        print(f"BlackColor: {black_color} {color('■', fore=black_color)}")
        print(f"WhiteColor: {white_color} {color('■', fore=white_color)}")
    else:
        print(f"'{preset_name}' というプリセットは存在しません。")

# ユーザーにカラーの変更を確認
fuchi_black_rgb, fuchi_white_rgb = get_custom_color_and_update("fuchi_pattern2")
base_black_rgb, base_white_rgb = get_custom_color_and_update("color_base2")
arrow_black_rgb, arrow_white_rgb = get_custom_color_and_update("color_yajirushi")
ability_black_rgb, ability_white_rgb = get_custom_color_and_update("ability_graph2")

#カラーのプレビュー
print("\n=== カラープレビュー ===")
for colors in color_presets:
    print_colors(colors)

print("\nカラー設定完了が完了しました。次のセルを実行してください。")
```

```python
# テキストカラーの定義(縁取りカラーのみ変更可)
import re
from colr import color

# RGB配列からHTMLなどに使われる16進数表現へ
# credit: https://qiita.com/ty21ky/items/05298d000be9a817d0cc
def rgb2hex(r,g,b):
    # r , g , b = 0 〜 255 # int型
    color = (r, g , b)
    html_color = '#%02X%02X%02X' % (color[0],color[1],color[2])
    return html_color

#ユーザから縁取りカラーを取得する関数
#1つ目の引数には名前、2つ目の引数にはデフォルト値のカラーコード
def get_outline_color_from_user(state_name, default_hex):
    pattern = re.compile(r"^#([A-Fa-f0-9]{6})$")
    while True:
        user_input = input(f"{state_name} の縁取りカラーコード（例: #00FFAA）を入力（空欄でデフォルト: {default_hex}）: ").strip()
        if user_input == "":
            user_input = default_hex
        if pattern.match(user_input):
            rgb = tuple(int(user_input[i:i+2], 16) for i in (1, 3, 5))
            # print(f"→ {state_name} outline color: {rgb}")
            return rgb
        else:
            print("無効な形式です。#RRGGBB の形式で入力してください。")

# テキストカラーの説明
print("ここでは文字色の縁取りカラーを指定できます。なお、内側のカラーはすでに定義済みです。")
print("freeはカーソル非選択時のテキストカラーです。暗めの色がオススメです。")
print("selectはカーソル選択時のテキストカラーです。明るめの色がオススメです。")
print("2つの値を入力値を表示した後で、変更したカラーのプレビューが表示されます。\n")

# デフォルト文字色
default_free_text = (220, 220, 220)
default_select_text = (255, 255, 255)

# ユーザー入力：縁取り色のみ
free_outline = get_outline_color_from_user("free", "#282828")
select_outline = get_outline_color_from_user("select", "#787878")

# カラー定義（スクリプト本体で使われる変数）
text_free_colors = (default_free_text, free_outline)
text_select_colors = (default_select_text, select_outline)

# common_w103_wifi_menu.brlyt用のテキストカラー定義(それ以外はBRLANで変更)
text_black_rgb, text_white_rgb = (text_select_colors[1], text_select_colors[0])

#カラーのプレビュー
#タプルを関数の引数として展開するために、*演算子を使用
print("\n=== カラープレビュー ===")
print(f"free(非選択時): {text_free_colors[1]} {color('■', fore=rgb2hex(*text_free_colors[1]))}")
print(f"select(選択時): {text_select_colors[1]} {color('■', fore=rgb2hex(*text_select_colors[1]))}")
```

## JSON5の編集(BRLYT)

### JSON5の文字列を変更

```sh
# オリジナルファイルをtmpフォルダに移動
!cp -r "/content/drive/MyDrive/8MeTools/BTRC/Assets/BRLYT/"* "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT/"
```

```python
import json5
import os
import re
from tqdm.notebook import tqdm

# JSON5ファイルが格納されているディレクトリ
json5_dir = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT"

# JSON5ファイルを再帰的に取得
json5_files = []
for root, _, files in os.walk(json5_dir):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

if not json5_files:
    tqdm.write("指定されたディレクトリにJSON5ファイルが存在しません。")
else:
    for json5_file in tqdm(json5_files, desc="Processing files"):
        file_path = json5_file

        with open(file_path, "r", encoding="utf-8") as file:
            json_text = file.read()

        # "name": 対象のブロックを検索
        pattern = re.compile(
            r'(\s*"name": "(fuchi_pattern2|color_base2|black_base2|pikapika|color_yajirushi|ability_graph2|black_pt00|black_pt01|text|active_text|chara02)".*?("tev color 1 a": \d+))',
            re.DOTALL
        )
        matches = list(re.finditer(pattern, json_text))

        if not matches:
            tqdm.write(f"{json5_file} に編集対象のTexture Paneが含まれていないため、編集を行いません。")
            continue

        # JSONテキストを変更
        for match in reversed(matches):  # **後ろから置換**
            block_text = match.group(1)
            block_name = match.group(2)

            # 対応するカラーを取得
            color_map = {
                "fuchi_pattern2": (fuchi_black_rgb, fuchi_white_rgb),
                "color_base2": (base_black_rgb, base_white_rgb),
                "black_base2": (base_black_rgb, base_white_rgb),
                "pikapika": (base_black_rgb, base_white_rgb),
                "color_yajirushi": (arrow_black_rgb, arrow_white_rgb),
                "ability_graph2": (ability_black_rgb, ability_white_rgb),
                "black_pt00": (ability_black_rgb, ability_white_rgb),
                "black_pt01": (ability_black_rgb, ability_white_rgb),
                "text": (text_black_rgb, text_white_rgb),
                "active_text": (text_black_rgb, text_white_rgb),
                "chara02": (arrow_white_rgb, arrow_black_rgb), # ここはあえて逆にしている.矢印のカラー割り当てをオリジナルに準拠するため.
            }

            black_rgb, white_rgb = color_map.get(block_name, ((0, 0, 0), (255, 255, 255)))

            # "tev color 0" のRGB値を変更
            block_text = re.sub(r'"tev color 0 r": \d+(,?)', f'"tev color 0 r": {black_rgb[0]}\\1', block_text)
            block_text = re.sub(r'"tev color 0 g": \d+(,?)', f'"tev color 0 g": {black_rgb[1]}\\1', block_text)
            block_text = re.sub(r'"tev color 0 b": \d+(,?)', f'"tev color 0 b": {black_rgb[2]}\\1', block_text)

            # "tev color 1" のRGB値を変更
            block_text = re.sub(r'"tev color 1 r": \d+(,?)', f'"tev color 1 r": {white_rgb[0]}\\1', block_text)
            block_text = re.sub(r'"tev color 1 g": \d+(,?)', f'"tev color 1 g": {white_rgb[1]}\\1', block_text)
            block_text = re.sub(r'"tev color 1 b": \d+(,?)', f'"tev color 1 b": {white_rgb[2]}\\1', block_text)

            # **変更を適用**
            json_text = json_text[:match.start()] + block_text + json_text[match.end():]

        # JSON5ファイルを上書き保存
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json_text)

        relative_path = os.path.relpath(json5_file, json5_dir)
        # tqdm.write(f"{relative_path} が変更されました。")
```

### JSON5をBRLYTに変換する

```python
import os
import subprocess
from tqdm.notebook import tqdm

# JSON5ファイルが格納されている親フォルダ
folder_path = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT"

# フォルダ内のすべてのJSON5ファイルを再帰的に取得
json5_files = []
for root, _, files in os.walk(folder_path):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

if not json5_files:
    tqdm.write("JSON5フォルダ内に処理対象のファイルがありません。")
else:
    tqdm.write("処理対象のファイル:")
    for file_path in json5_files:
        relative_path = os.path.relpath(file_path, folder_path)
        tqdm.write(relative_path)
    tqdm.write("\n")

    for file_path in tqdm(json5_files, desc="Processing files"):
        # wuj5.py を実行
        # relative_path = os.path.relpath(file_path, folder_path)
        command = ["python", "wuj5.py", "encode", file_path]
        # print(f"実行中: {' '.join(command).replace(folder_path, '.')}") # 簡略化して表示

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            # エラーが発生した場合のみ詳細情報を出力
            tqdm.write(f"エラー発生: {os.path.basename(file_path)}")
            tqdm.write(f"コマンド: {' '.join(command)}")
            tqdm.write(f"エラー出力: {e.stderr}")

    print("\nすべてのJSON5ファイルをエンコードしました！")
```

### JSON5を削除して、BRLYTのみにする

```python
#json5を削除
import os

# JSON5ファイルが格納されている親フォルダ
folder_path = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT"

# フォルダ内のすべてのJSON5ファイルを再帰的に取得
json5_files = []
for root, _, files in os.walk(folder_path):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

if not json5_files:
    print("削除対象のJSON5ファイルがありません。")
else:
    for json5_file in json5_files:
        file_path = os.path.join(folder_path, json5_file)
        os.remove(file_path)
        # デバッグ
        # print(f"削除完了: {json5_file}")
    print("すべてのJSON5ファイルを削除しました。")
```

```sh
#一時フォルダから完成フォルダに移動(BRLYT)
!mv "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLYT/"* "/content/drive/MyDrive/8MeTools/BTRC/EditedBRLYT/"
print("BRLYTファイルへの変換が全て完了しました。Googleドライブから確認してください。")
```

## JSON5の編集(BRLAN)

```python
# JSON5ファイルをtmpフォルダに移動
!cp -r "/content/drive/MyDrive/8MeTools/BTRC/Assets/BRLAN/"* "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN/"
```

### JSON5の文字列の編集

```python
import json5
import os
from tqdm.notebook import tqdm

json5_dir = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN"
json5_files = []
for root, _, files in os.walk(json5_dir):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

# カラー更新関数
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

                    color_type = kind.split()[2]  # '0' or '1'
                    component = kind.split()[-1]  # 'r', 'g', 'b'

                    for key in target.get("keys", []):
                        # 遷移なし（同じ色で固定）
                        if start_outline == end_outline and start_text == end_text:
                            color = start_text if color_type == "0" else start_outline
                        else:
                            # 遷移あり（frame に応じて始点か終点の色を選ぶ）
                            color = start_text if (color_type == "0" and key["frame"] == 0.0) else \
                                    end_text if (color_type == "0" and key["frame"] != 0.0) else \
                                    start_outline if (color_type == "1" and key["frame"] == 0.0) else \
                                    end_outline

                        if component == "r":
                            key["value"] = color[0]
                        elif component == "g":
                            key["value"] = color[1]
                        elif component == "b":
                            key["value"] = color[2]
    return data

# 実行
if not json5_files:
    tqdm.write("指定されたディレクトリにJSON5ファイルが存在しません。")
else:
    for json5_file in tqdm(json5_files, desc="Processing files"):
        relative_path = os.path.relpath(json5_file, json5_dir)
        with open(json5_file, "r", encoding="utf-8") as file:
            try:
                data = json5.load(file)
            except Exception as e:
                tqdm.write(f"{relative_path}: 読み込みエラー - {e}")
                continue

        filename = os.path.basename(json5_file).lower()

        # ファイル名ルールによるカラー適用順
        if "free_to_select" in filename:
            start_outline, start_text = text_free_colors
            end_outline, end_text = text_select_colors
        elif "select_to_free" in filename:
            start_outline, start_text = text_select_colors
            end_outline, end_text = text_free_colors
        elif "free" in filename and "select" not in filename:
            start_outline = end_outline = text_free_colors[0]
            start_text = end_text = text_free_colors[1]
        elif "select" in filename and "free" not in filename:
            start_outline = end_outline = text_select_colors[0]
            start_text = end_text = text_select_colors[1]
        elif "stop" in filename:
            start_outline = end_outline = text_select_colors[0]
            start_text = end_text = text_select_colors[1]
        elif "common_w098_wifi_menu_text" in filename:
            start_outline = end_outline = text_select_colors[0]
            start_text = end_text = text_select_colors[1]
        elif "common_w010_cup_fuchi_off" or "common_w010_cup_fuchi_on_to_off" in filename:
            start_outline = end_outline = text_select_colors[0]
            start_text = end_text = text_select_colors[1]
        elif "fuchi_check_loop" in filename:
            continue
        else:
            tqdm.write(f"{json5_file}: ファイル名から適用カラーが判断できません。スキップします。")
            continue

        # 更新
        updated_data = update_tev_colors(data, start_outline, start_text, end_outline, end_text)

        # 保存
        with open(json5_file, "w", encoding="utf-8") as file:
            json5.dump(updated_data, file, indent=2)

        relative_path = os.path.relpath(json5_file, json5_dir)
        # tqdm.write(f"{relative_path} の編集が完了しました。")
```

## JSON5をBRLANに変換するコード

```python
# json5をBRLANに変換
import os
import subprocess
from tqdm.notebook import tqdm

# JSON5ファイルが格納されている親フォルダ
folder_path = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN"

# フォルダ内のすべてのJSON5ファイルを再帰的に取得
json5_files = []
for root, _, files in os.walk(folder_path):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

if not json5_files:
    tqdm.write("JSON5フォルダ内に処理対象のファイルがありません。")
else:
    tqdm.write("処理対象のファイル:")
    for file_path in json5_files:
        relative_path = os.path.relpath(file_path, folder_path)
        tqdm.write(relative_path)
    tqdm.write("\n")

    for file_path in tqdm(json5_files, desc="Processing files"):
        # wuj5.py を実行
        # relative_path = os.path.relpath(file_path, folder_path)
        command = ["python", "wuj5.py", "encode", file_path]
        # tqdm.write(f"実行中: {' '.join(command).replace(folder_path, '.')}") # 簡略化して表示

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            # エラーが発生した場合のみ詳細情報を出力
            tqdm.write(f"エラー発生: {os.path.basename(file_path)}")
            tqdm.write(f"コマンド: {' '.join(command)}")
            tqdm.write(f"エラー出力: {e.stderr}")

    tqdm.write("\nすべてのJSON5ファイルをエンコードしました！")
```

### JSON5ファイルの削除

```python
#json5を削除
import os

# JSON5ファイルが格納されている親フォルダ
folder_path = "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN"

# フォルダ内のすべてのJSON5ファイルを再帰的に取得
json5_files = []
for root, _, files in os.walk(folder_path):
    for f in files:
        if f.endswith(".json5"):
            json5_files.append(os.path.join(root, f))

if not json5_files:
    print("削除対象のJSON5ファイルがありません。")
else:
    for json5_file in json5_files:
        file_path = os.path.join(folder_path, json5_file)
        os.remove(file_path)
        # デバッグ用
        # print(f"削除完了: {json5_file}")
    print("すべてのJSON5ファイルを削除しました。")
```

```sh
#一時フォルダから完成フォルダに移動
!mv "/content/drive/MyDrive/8MeTools/BTRC/tmp/BRLAN/"* "/content/drive/MyDrive/8MeTools/BTRC/EditedBRLAN/"
print("BRLANファイルへの変換が全て完了しました。Googleドライブから確認してください。")
```
