# WUJ5 Python Encode 改善フロー

本書は、`wuj5` を Rust へ移植する前に、Python 実装のまま `.json5` から `.brlyt` / `.brlan` へ変換する処理を見直すための実装フローをまとめたものです。

今回の対象は以下の 3 点です。

1. `wuj5.py` の処理を Python API と CLI に分離する
2. `btrc/encode.py` から subprocess 呼び出しを外す
3. 実行時間を再計測し、次の改善対象を判断できる状態にする

Rust 化は本フローの対象外です。ただし、将来 Rust 実装へ差し替えやすいように、`btrc` から見える呼び出し境界は先に整理します。

---

## 1. 背景

現在の `btrc` の encode 処理は、JSON5 ファイルごとに以下のような subprocess を起動しています。

```py
command = ["python", str(wuj5_script), "encode", file_path]
subprocess.run(command, capture_output=True, text=True, check=True)
```

この方式では、各ファイルの変換処理そのものに加えて、Python インタプリタ起動、`wuj5.py` の import、引数処理、プロセス生成のコストが毎回発生します。

BRLYT / BRLAN の JSON5 ファイル数が多い場合、この固定コストが全体時間に大きく影響する可能性があります。

---

## 2. 目的

- `btrc` から `wuj5` を Python ライブラリとして直接呼べるようにする
- CLI と変換ロジックを分離し、テストしやすくする
- subprocess 起動回数を 0 にする
- 改善前後の実行時間を比較できるようにする
- Rust 化が必要かどうかを、計測結果から判断できる状態にする

---

## 3. 非目的

- Rust 実装の追加
- BRLYT / BRLAN のフォーマット仕様変更
- JSON5 のデータ構造変更
- `btrc` のカラー更新ロジック変更
- Notebook / CLI のユーザー体験変更

---

## 4. 現状の呼び出し構造

現在の主な流れは以下です。

```text
main.py
  -> btrc.encode.encode_json5_files(...)
    -> subprocess.run(["python", "wuj5/wuj5.py", "encode", path])
      -> wuj5/wuj5.py
        -> json5.loads(...)
        -> pack_brlyt(...) / pack_brlan(...)
        -> binary write
```

問題は、`pack_brlyt` / `pack_brlan` が Python 関数として存在しているにもかかわらず、`btrc` からは直接呼ばず、毎回 CLI 経由になっている点です。

目標の構造は以下です。

```text
main.py
  -> btrc.encode.encode_json5_files(...)
    -> wuj5.api.encode_file(...)
      -> json5.loads(...)
      -> pack_brlyt(...) / pack_brlan(...)
      -> binary write
```

CLI は互換性維持のため残します。

```text
wuj5/wuj5.py
  -> wuj5.api.encode_file(...) / decode_file(...)
```

---

## 5. 推奨する最終構成

```text
wuj5/
  __init__.py
  api.py
  wuj5.py
  common.py
  brlyt.py
  brlan.py
  brctr.py
  bmg.py
  u8.py
  yaz.py
```

### `wuj5/api.py`

Python ライブラリとして使うための公開入口を置きます。

想定する最小 API は以下です。

```py
def encode_file(in_path, out_path=None, retained=None, renamed=None):
    ...

def decode_file(in_path, out_path=None, retained=None, renamed=None):
    ...

def encode_json5_file(in_path, out_path=None):
    ...
```

最初は `wuj5/wuj5.py` にある既存の `encode` / `decode` 系関数を移動、または薄くラップする形で十分です。

### `wuj5/wuj5.py`

CLI 専用にします。

責務は以下に限定します。

- `argparse` で引数を読む
- 入力数と出力数を検証する
- `wuj5.api` の関数を呼ぶ
- CLI 用の終了コードやエラーメッセージを扱う

### `btrc/encode.py`

subprocess をやめ、`wuj5.api.encode_file` を直接呼びます。

`wuj5_script` 引数は互換性のため一時的に残してもよいですが、最終的には不要になります。

---

## 6. 実装フェーズ

### フェーズ1: 計測ポイントを入れる

目的: 変更前後の差分を見られるようにする。

最低限、以下の時間を分けて確認します。

- BRLYT JSON5 更新
- BRLAN JSON5 更新
- encode 全体
- ファイル数

可能であれば、encode 内も以下に分けます。

- JSON5 read
- `json5.loads`
- `pack_brlyt` / `pack_brlan`
- binary write

この段階では実装を大きく変えず、現状の時間を記録します。

### フェーズ2: `wuj5` を import 可能にする

目的: `btrc` から `wuj5` を Python パッケージとして呼べるようにする。

実施内容:

- `wuj5/__init__.py` を追加する
- `wuj5/api.py` を追加する
- `wuj5` 内の import を相対 import に寄せる
  - 例: `from common import *` から `from .common import *`
  - CLI として直接実行する場合の扱いは別途確認する

注意点:

- 既存の `python wuj5/wuj5.py encode ...` が動かなくなる可能性がある
- 互換性を保つなら、CLI は `python -m wuj5.wuj5 encode ...` を正式ルートにする
- 既存ドキュメントや Notebook の呼び出し方法も後で合わせる

### フェーズ3: API と CLI を分離する

目的: 変換ロジックを CLI から独立させる。

実施内容:

- `wuj5/wuj5.py` から `decode` / `encode` / `decode_u8` / `encode_u8` などを `wuj5/api.py` へ移す
- `wuj5/wuj5.py` は `argparse` と API 呼び出しだけにする
- CLI の挙動が変わらないことを確認する

確認観点:

- `.brlyt.json5` から `.brlyt` が生成される
- `.brlan.json5` から `.brlan` が生成される
- 出力先未指定時のパスが従来通りになる
- 未知拡張子で従来通り失敗する

### フェーズ4: `btrc/encode.py` から subprocess を外す

目的: ファイルごとの Python プロセス起動をなくす。

変更前:

```py
command = ["python", str(wuj5_script), "encode", file_path]
subprocess.run(command, capture_output=True, text=True, check=True)
```

変更後のイメージ:

```py
from wuj5.api import encode_file


def encode_json5_files(files, wuj5_script=None):
    if not files:
        print(t("no_json5"))
        return

    for file_path in files:
        try:
            encode_file(file_path)
        except Exception as e:
            print(f"エラー: {file_path}")
            print(e)

    print(t("done_encode"))
```

`wuj5_script` はこの時点では未使用になります。外部 API 互換を守るため、一度残してから後続で削除するのが安全です。

### フェーズ5: 再計測する

目的: subprocess 排除でどの程度改善したか確認する。

確認する指標:

- encode 全体時間
- 1ファイルあたり平均時間
- BRLYT / BRLAN 別の時間
- 失敗ファイル数
- 出力ファイルの byte 差分

期待する結果:

- 小さい JSON5 ファイルが多い場合、改善幅が大きい
- 大きい JSON5 ファイルが多い場合、`json5.loads` や pack 処理が次の支配要因になる

---

## 7. テスト方針

最初に必要なテストは、変換結果が壊れていないことを確認するものです。

### 単体テスト

- `wuj5.api.encode_file` が `.brlyt.json5` を受けて `.brlyt` を出力する
- `wuj5.api.encode_file` が `.brlan.json5` を受けて `.brlan` を出力する
- `out_path` 指定時に指定先へ出力する
- 未知拡張子で例外になる

### 回帰テスト

既存 CLI と新 API の出力が一致することを確認します。

```text
old: python wuj5/wuj5.py encode sample.brlyt.json5
new: wuj5.api.encode_file("sample.brlyt.json5")
```

比較は byte-for-byte で行います。

### `btrc` 側テスト

- `encode_json5_files` が `wuj5.api.encode_file` を呼ぶこと
- 空リストで `no_json5` を表示して終了すること
- 1ファイルが失敗しても他ファイルの処理を継続すること

---

## 8. 互換性の扱い

### 残したい互換性

- `python -m wuj5.wuj5 encode path/to/file.brlyt.json5`
- `python -m wuj5.wuj5 decode path/to/file.brlyt`
- `btrc.encode.encode_json5_files(files, WUJ5_SCRIPT)`

### 廃止候補

- `python wuj5/wuj5.py encode ...`
- `btrc.encode.encode_json5_files(files, wuj5_script)` の `wuj5_script` 引数

廃止する場合は、先に README / Notebook / docs の呼び出し例を更新します。

---

## 9. リスクと注意点

- `wuj5` 内の import を相対 import に変えると、直接スクリプト実行の挙動が変わる
- `sys.exit(...)` を API 内に残すと、`btrc` 実行全体が終了してしまう
- API 化する場合は、`sys.exit` より例外を投げる方が扱いやすい
- subprocess では分離されていた例外が、同一プロセス内で伝播するようになる
- 既存の JSON5 出力フォーマットやバイナリ出力を変えないようにする

特に `sys.exit` は API 化の障害になりやすいため、可能であれば段階的に `ValueError` などへ置き換えます。

---

## 10. 完了条件

このフローの完了条件は以下です。

- `wuj5.api.encode_file` から `.brlyt.json5` / `.brlan.json5` を encode できる
- `wuj5/wuj5.py` は CLI として従来相当の encode / decode ができる
- `btrc/encode.py` が subprocess を使わない
- 既存テストが通る
- 追加した encode 関連テストが通る
- 改善前後の encode 時間を比較できる記録がある

---

## 11. 次の判断

このフロー完了後、再計測結果を見て次の改善対象を決めます。

- subprocess 排除だけで十分速い場合
  - Rust 化は保留
  - テストとドキュメント整備を優先

- `json5.loads` / `json5.dump` が支配的な場合
  - JSON5 入出力回数の削減を検討
  - BRLYT のように文字列編集で済む箇所は parse を避ける

- `pack_brlyt` / `pack_brlan` が支配的な場合
  - Python 実装の `bytes` 連結を見直す
  - それでも不足する場合に Rust 移植を再検討する

Rust 化を検討する場合も、この API 境界を維持すれば、`wuj5.api` の内部だけを差し替える形にできます。
