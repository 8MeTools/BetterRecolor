# クイックスタート

実行方法は 2 通りあります。

| 方法 | 向いている人 |
| --- | --- |
| Google Colab | 環境構築なしでブラウザから使いたい人 |
| ローカル実行 | 手元の PC で繰り返し調整したい人 |

どちらの方法でも、基本の入出力は同じです。

| 種類 | 場所 |
| --- | --- |
| 入力 | `Assets/BRLYT` と `Assets/BRLAN` |
| 色設定 | `color_config.json` |
| 出力 | `Output` |

## Google Colab で使う

1. GitHub 上の `BetterRecolor.ipynb` を Colab で開きます。
2. セットアップ用セルだけを先に実行します。
3. `/content/BetterRecolor/color_config.json` を編集します。
4. 残りのセルを上から順番に実行します。
5. 生成された `Output.zip` をダウンロードします。

::: warning
Colab のセットアップ用セルは、既存の `/content/BetterRecolor` を削除してから再取得します。
編集済みの `color_config.json` や入力ファイルを置いている場合は、先に Google Drive などへ退避してください。
:::

## ローカルで使う

Python 3.11 以上を推奨します。

```sh
pip install -r requirements.txt
python main.py
```

入力を省略して日本語で実行する場合は、次のように指定できます。

```sh
python main.py --lang ja --yes
```

WSL2 では `python3 main.py` を使用してください。

## 色設定

`color_config.json` では、主に次の項目を編集します。

| 項目 | 内容 |
| --- | --- |
| `presets` | BRLYT 側で使用する色 |
| `outline.free` | 通常時の BRLAN 側の縁取り色 |
| `outline.select` | 選択時の BRLAN 側の縁取り色 |

色はすべて `#RRGGBB` 形式で指定します。

## 出力後にすること

1. `Output` または `Output.zip` から生成ファイルを取り出します。
2. 必要な `*.d` フォルダを元のアセットへ上書きします。
3. [Wiimms SZS Tool](https://szs.wiimm.de/wszst/) で SZS に再パックします。
4. ゲーム内で表示を確認します。

## 注意点

- ローカル実行では、`tmp` と `Output` は実行ごとに作り直されます。
- Colab では、セットアップを再実行すると `/content/BetterRecolor` 配下のファイルが削除されます。
- マルチプレイ時の一部ボタン色は、プレイヤー識別のため意図的に変更されない場合があります。
