# WSL2 で実行する

最終更新日: 2026年4月4日

このページでは、WSL2 上で BetterRecolor を実行するための手順を説明します。

Windows や macOS と基本的な流れは同じですが、Ubuntu / Debian 系の Python では PEP 668 により、システム環境へ直接パッケージをインストールできない場合があります。そのため、ここでは `venv` で仮想環境を作成して実行します。

## 対象読者

- WSL2 を利用している
- WSL2 上で BetterRecolor を動かしたい
- 基本的な Linux コマンドの操作ができる

::: warning
以降のコマンドは WSL2 のターミナル上で実行します。PowerShell やコマンドプロンプトではありません。
:::

## 確認環境

以下の環境で動作確認しています。

- Windows 11 Home 64-bit
- WSL2 Ubuntu 24.04 LTS
- Python 3.12.2

## 事前準備

WSL2 に Python、pip、venv をインストールしておきます。

参考: [WSL2でPython,pip,venvをインストールして仮想環境を作成](https://zenn.dev/ak_yoshimatsu/articles/69457d3f44fe55)

## 手順

### 1. リポジトリをクローンする

```bash
git clone https://github.com/8MeTools/BetterRecolor.git
```

### 2. ディレクトリへ移動する

```bash
cd path/to/BetterRecolor
```

`path/to/BetterRecolor` は、実際にクローンしたディレクトリに置き換えてください。

### 3. 仮想環境を作成する

```bash
python3 -m venv .btrc
```

BetterRecolor のディレクトリ内に `.btrc` という仮想環境が作成されます。

確認する場合は、隠しファイルも表示します。

```bash
ls -la
```

### 4. 仮想環境を有効化する

```bash
source .btrc/bin/activate
```

有効化されると、プロンプトの先頭に `(.btrc)` が表示されます。

```bash
(.btrc) user@hostname:~/path/to/BetterRecolor$
```

### 5. 依存関係をインストールする

仮想環境が有効な状態で実行します。

```bash
pip install -r requirements.txt
```

### 6. BetterRecolor を実行する

```bash
python3 main.py
```

起動後は、表示される案内に従って言語選択と色設定の確認を行います。

入力を省略して実行したい場合は、次のように指定できます。

```bash
python3 main.py --lang ja --yes
```

### 7. 仮想環境を無効化する

作業が終わったら、次のコマンドで仮想環境を無効化できます。

```bash
deactivate
```

プロンプトから `(.btrc)` が消えれば無効化されています。

## 2回目以降の実行

2回目以降は、リポジトリへ移動して仮想環境を有効化してから実行します。

```bash
cd path/to/BetterRecolor
source .btrc/bin/activate
python3 main.py
```

## 補足

WSL2 では、システム全体へ Python パッケージを直接インストールするよりも、プロジェクトごとに仮想環境を作成する方法が推奨されます。BetterRecolor でも、依存関係は `.btrc` の中へインストールしておくと管理しやすくなります。

