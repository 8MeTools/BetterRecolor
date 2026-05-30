[![CI](https://github.com/8MeTools/BetterRecolor/actions/workflows/ci.yml/badge.svg)](https://github.com/8MeTools/BetterRecolor/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# BetterRecolor

このドキュメントは日本語で書かれています。英語版は [README.md](README.md) を参照してください。

## 概要

ゲーム内で表示されるボタンやテキストの**色を一括で編集できるツール**です。  
JSON / JSON5 形式にデコードされたファイルを編集し、BRLYT（レイアウトファイル）とBRLAN（アニメーションファイル）としてエンコードします。Google Colabでもローカル環境でも使用できます。

## はじめに

Google Colaboratoryを初めて利用する方は、以下の動画を参考にしてください。

- [【研究生活ハック】Google Colabの使い方](https://youtu.be/j2p9pLGHRPg?si=_Q9bPEW3dKxtqkcs)

### Colabの利点

- **実行環境に依存しない**  
   クラウド上の割り当てられたマシンで処理を実行するため、個人のPC環境に左右されません。
- **環境構築不要**  
   ブラウザ上でコードを実行できるため、Pythonのインストールやライブラリのセットアップが不要です。Pythonの知識がない方でも、セルをクリックするだけでツールを利用できます。

## 使い方

実行方法は次の2通りです。

- **Google Colabで実行**: 環境構築なしで使いたい方向け
- **ローカルで実行**: 手元のPCで繰り返し実行したい方向け

どちらの方法でも、入力・出力の考え方は同じです。

- 入力元: `Assets/BRLYT` と `Assets/BRLAN`
- 出力先: `Output`
- 色設定ファイル: `color_config.json`

### 1. Google Colabで実行する

1. **ノートブックをColabで開く**

   リポジトリの [BetterRecolor.ipynb](BetterRecolor.ipynb) を開き、Colabの「Open in Colab」から実行します。
> [!WARNING]
> 操作に自信がない限りは、毎回GitHub上からノートブックを開いてください。このリポジトリは頻繁に更新される可能性があるため、Googleドライブ内にクローンされたノートブックを開いて実行すると、正常に動作しない可能性があります。


2. **セットアップ用セルを先に実行する**

   次の準備処理が完了するところまで実行します。

   - `/content/BetterRecolor` の再取得（既存の `/content/BetterRecolor` は削除されてから再クローンされます）
   - Colab実行に不要な開発用ファイルの削除
   - `requirements.txt` で依存関係をインストール

> [!WARNING]
> Colabのセットアップ用セルは、既存の `/content/BetterRecolor` フォルダを削除してからクローンします。
> `/content/BetterRecolor` に編集済みの `color_config.json` や入力ファイルを置いている場合は、セットアップ前にダウンロードするか、Google Driveなど別の場所にコピーしておき、セットアップ後に戻してください。
> ただし、JSONファイルの構造に変更が入る可能性もあるため、セットアップ後はGitHub上の最新の `color_config.json` を確認してから編集することを推奨します。

   依存関係のインストールが正常に完了すると、次のようなメッセージが表示されます。

   ```
   ✅Setup complete! Open color_config.json to edit.
   ```

> [!WARNING]
> セットアップ用セルは最初の数個だけです。最後まで実行しないように注意してください。

3. **`color_config.json` を編集する**

   `/content/BetterRecolor/color_config.json` を編集します。
   - `presets`: BRLYT側で使用する色
   - `outline.free` / `outline.select`: BRLAN側で使用する縁取り色
   - すべて `#RRGGBB` 形式で指定

> [!NOTE]
> Colabの左側のファイルタブから `content` → `BetterRecolor` と進み、`color_config.json` をダブルクリックして編集モードに入ることができます。


4. **残りのセルを上から順番に実行する**

   セル内で次の処理が行われます。

   - 色設定の読み込みと反映
   - `Output` への出力

   途中で色設定の確認が表示されたら、内容を確認して続行します。

   実行時の入力を省略したい場合は、ノートブック内の実行セルを次のように変更できます。

   ```sh
   !python main.py --lang ja --yes
   ```

   - `--lang ja`: 言語選択を省略して日本語で実行
   - `--yes` / `-y`: 色設定の確認に自動で yes と回答

5. **生成物を取得する**

   最後のセルを実行すると、`Output` フォルダが `Output.zip` に圧縮され、ブラウザからダウンロードできます。

6. **ゲーム用アセットへ反映する**

   ダウンロードしたファイルを展開し、必要な `*.d` フォルダを元のアセットへ上書きコピーします。

7. **SZS化して動作確認する**

   [Wiimms SZS Tool](https://szs.wiimm.de/wszst/) で再パックして、ゲーム内で表示を確認します。

### 2. ローカルで実行する

#### 前提

- Python 3.11以上推奨
- プロジェクト直下に `Assets` フォルダがあり、`BRLYT` / `BRLAN` が配置されていること

#### 手順

1. **依存関係をインストールする**

   ```sh
   pip install -r requirements.txt
   ```

2. **色設定ファイルを編集する**

   `color_config.json` を編集します。

   - `presets`: BRLYT側で使用する色
   - `outline.free` / `outline.select`: BRLAN側で使用する縁取り色
   - すべて `#RRGGBB` 形式で指定

3. **ツールを実行する**

   ```sh
   python main.py
   ```

   WSL2環境で実行する場合は、`python3` コマンドを使用してください。

   ```sh
   python3 main.py
   ```

   入力を省略して実行する場合は、次のオプションを使用できます。

   ```sh
   python main.py --lang ja --yes
   ```

   - `--lang ja` / `--lang en`: 起動時の言語選択を省略
   - `--yes` / `-y`: 色設定の確認に自動で yes と回答

4. **言語を選択し、設定を確認する**

   起動時に `Language / 言語 (ja/en) [ja]:` と表示されます。`ja` か `en` を入力してください。

   続いて色設定のプレビューが表示されるので、`Y/N` で実行可否を選択します。

5. **出力結果を確認する**

   処理完了後、`Output` にファイルが出力されます。出力には、生成されたファイルと `pack-guide.txt` が含まれます。

#### 再実行時の注意

- （ローカル環境）実行時に `tmp` / `Output` は毎回作り直されます。以前の出力を残したい場合は、実行前に別フォルダへ退避してください。
- （Colab 環境）セットアップ用セルを再実行すると、`/content/BetterRecolor` フォルダ自体が削除されて再取得されます。そのフォルダ直下に `Assets` や編集済みの `color_config.json` などを置いている場合、それらもまとめて消えるため、必ず Google Drive や `/content/drive` など再取得の影響を受けない場所に保存してください。

## 開発者向け

### Lint / Test

```sh
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest
```

### Colab バッジの更新

`BetterRecolor.ipynb` 内の Colab バッジ URL は、`colab_badge.json` から生成します。
GitHub の owner、repository、branch、notebook path を変更する場合は、`colab_badge.json` を編集してから次を実行してください。

```sh
python scripts/update_colab_badge.py
```

このスクリプトは、Colab バッジを含む markdown セルだけを更新します。

### リリース運用（CalVer）

日付+連番のバージョン形式を使用します。例: `26.01.28.1`

1. バージョン更新

   ```sh
   python scripts/bump_version.py
   ```

2. タグ作成

   ```sh
   python scripts/bump_version.py --tag
   ```

3. タグ作成 + push（CI成功後にReleaseが作成されます）

   ```sh
   python scripts/bump_version.py --tag --push
   ```

### CI / Release 条件

- CI: `push` と `pull_request` で `ruff check .` と `pytest` が実行されます。
- Release: CIが成功したコミットに付いた `v*` タグ（例: `v26.01.28.1`）がある場合のみ作成されます。

## よくある質問

### Q. 実行するセルの順番を間違えてしまった場合、どうすればよいですか？

**A.** Colabの使用に自信がない場合は、次の手順を実行してやり直してください。\
画面左上のメニューバーから「**ランタイム**」を選択し、「**ランタイムを接続解除して削除**」を実行してください。セルの実行順序に注意して、最初から実行してください。

### Q. マルチプレイ時、一部のボタンが指定された色に変わっていません。

**A.** マルチプレイヤーでのボタンカラー変更は、プレイヤーごとの識別が困難になるため、意図的に変更していません。ご了承ください。

## 不具合について

- GitHubのIssuesにてお知らせください。

## Third-Party

このリポジトリには MIT ライセンスの[wuj5](https://github.com/stblr/wuj5)を同梱しています。ライセンスは `wuj5/LICENSE` を参照してください。
