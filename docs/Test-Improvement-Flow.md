# テストコード改善フロー

このドキュメントは、現在の BetterRecolor のテストを整理し、段階的に強化するための作業フローをまとめたものです。

目的は、単にテスト数を増やすことではなく、壊れやすい処理、ファイル破壊につながる処理、ユーザー操作に近い処理を優先して守ることです。

## 現状

現在のテストは以下を中心にカバーしています。

- `btrc.colors`
  - `color_config.json` の読み込み
  - 必須キー不足
  - HEX値の検証
  - ファイル未存在
  - 実行確認入力
- `btrc.brlan`
  - `update_tev_colors`
  - `select_color_rule`
  - 一部の実アセット由来データ
- `btrc.brlyt`
  - `apply_tev_colors`
  - 一部の実アセット由来データ
- `btrc.cleanup`
  - `move_all_files` のディレクトリマージ

一方で、以下はまだ薄い、または未カバーです。

- `btrc.json_io`
- `btrc.encode`
- `btrc.cleanup.remove_json_files`
- `btrc.i18n`
- `main.py` の実行フロー
- BRLYT / BRLAN の境界ケース
- 実アセット依存テストと安定した単体テストの分離

## 基本方針

- まずユニットテストで小さく固める。
- 外部ツールや実アセットに依存するテストは後段に分ける。
- ファイル操作は必ず `tmp_path` で完結させる。
- `main.py` は重いE2Eにせず、依存関数を `monkeypatch` して呼び出し順と早期終了を確認する。
- 既存の正常動作を変えずに、回帰検知の範囲を増やす。

## 推奨ディレクトリ構成

当面は既存の `tests/` 直下でよいですが、実アセット依存が増えたら分離します。

```text
tests/
  conftest.py
  test_brlan.py
  test_brlyt.py
  test_cleanup.py
  test_colors_json.py
  test_json_io.py
  test_encode.py
  test_i18n.py
  test_main_flow.py
  integration/
    test_assets_brlan.py
    test_assets_brlyt.py
```

`integration/` は後からで構いません。まずは skip されない小さいユニットテストを優先します。

## フェーズ1: I/Oとファイル操作を固める

優先度: 高

対象:

- `btrc.json_io.list_layout_json_files`
- `btrc.json_io.read_layout_json`
- `btrc.json_io.write_layout_json`
- `btrc.cleanup.remove_json_files`
- `btrc.cleanup.move_all_files`

追加するテスト:

- `.json` と `.json5` の両方を列挙できる。
- `.txt` や `.brlyt` など対象外ファイルを列挙しない。
- ネストしたディレクトリ配下のJSONを拾える。
- `.json` は標準 `json` として読める。
- `.json5` はコメントや末尾カンマを含んでも読める。
- `write_layout_json` で書いた内容を再読込できる。
- `remove_json_files` が指定ファイルだけ削除する。
- `move_all_files` が既存ファイルを上書きできる。
- `move_all_files` が既存ディレクトリを壊さずマージできる。

完了条件:

- 実アセットなしで全テストが通る。
- ファイル作成・削除・移動はすべて `tmp_path` 内で完結している。

## フェーズ2: encodeをモックで検証する

優先度: 高

対象:

- `btrc.encode.encode_layout_json_files`
- timing集計系の補助関数

追加するテスト:

- 空リストなら `count=0` で終了する。
- `encode_file` が各ファイルに対して呼ばれる。
- `encode_file` の戻り値が `timings` に入る。
- `ext` ごとの集計が作られる。
- 途中で例外が出ても、他ファイルの処理が継続される。
- 例外数が `failed` に反映される。

方針:

- `wuj5.api.encode_file` を直接動かさない。
- `monkeypatch` で `btrc.encode.encode_file` を差し替える。
- print内容の完全一致は避け、戻り値を主に検証する。

完了条件:

- 外部変換器なしで encode の制御フローを検証できる。
- 成功、失敗、空入力の3系統がある。

## フェーズ3: BRLANロジックの境界ケースを増やす

優先度: 中

対象:

- `btrc.brlan.update_tev_colors`
- `btrc.brlan.select_color_rule`

追加するテスト:

- `r/g/b` すべての成分が更新される。
- `a` 成分は更新されない。
- `name != "text"` の content は変更されない。
- `sections`、`contents`、`animations`、`targets` が空または欠けていても落ちない。
- `fuchi_check_loop` は `None` を返す。
- `stop`、`common_w098_wifi_menu_text`、`common_w010_cup_fuchi_off`、`common_w010_cup_fuchi_on_to_off` の例外ルールを確認する。

注意:

- `kind` の形式が壊れているケースは、現在の実装では落ちる可能性があります。
- その挙動を許容するか、防御的に直すかを決めてからテスト化します。

完了条件:

- 色成分ごとの分岐が最低1回ずつ検証されている。
- ファイル名ルールの例外が明示的にテスト名に出ている。

## フェーズ4: BRLYTロジックの正規表現仕様を固定する

優先度: 中

対象:

- `btrc.brlyt.apply_tev_colors`

追加するテスト:

- 複数ブロックをすべて更新する。
- 対象外ブロックは変更しない。
- `color_map` に無い対象名はデフォルト色になる。
- `tev color 1 a` が無いブロックは対象外になる。
- `r/g/b` は更新し、`a` は維持する。
- カンマ有無を保ったまま更新する。

注意:

- 現在のBRLYT処理は正規表現ベースです。
- JSON構造として厳密に扱うテストではなく、現行仕様の文字列置換として検証します。

完了条件:

- 正規表現の対象範囲がテストで固定されている。
- 意図しないブロックを巻き込まないことが確認されている。

## フェーズ5: colorsの補助関数と表示を補う

優先度: 中

対象:

- `hex_to_rgb`
- `rgb_to_hex`
- `propagate_dependent_presets`
- `build_color_map_from_presets`
- `print_loaded_color_preview`
- `print_preset`

追加するテスト:

- HEXとRGBの相互変換。
- 依存プリセットが伝播する。
- `build_color_map_from_presets` が全キーを返す。
- 表示系は `print` を monkeypatch して、落ちないことと主要キーの出力だけ確認する。

完了条件:

- `load_color_settings_from_json` の大きいテストだけに依存せず、補助関数単位でも失敗箇所が分かる。

## フェーズ6: i18nを固定する

優先度: 中

対象:

- `btrc.i18n.set_locale`
- `btrc.i18n.t`
- `_parse_simple_yaml`

追加するテスト:

- `set_locale("ja")` と `set_locale("en")` で既知キーが取得できる。
- 未知キーはキー名そのものを返す。
- 簡易YAMLパーサが単純な `lang: key: value` 形式を読める。
- コメント行と空行を無視できる。

注意:

- 外部 `i18n` ライブラリの有無で挙動が変わりうるため、公開APIの結果を中心に確認します。

完了条件:

- メッセージキーのリネーム時にテストで検知できる。

## フェーズ7: mainフローを薄く統合テストする

優先度: 中

対象:

- `main.choose_locale`
- `main.copy_all`
- `main.reset_dir`
- `main.main`

追加するテスト:

- `choose_locale` は `ja/en` 以外なら `ja` に戻る。
- `copy_all` は階層構造を保ってコピーする。
- `reset_dir` は既存ディレクトリを空にして再作成する。
- 設定読み込み失敗時に後続処理を呼ばず終了する。
- ユーザーが適用を拒否した場合、tmpやOutputを触る前に終了する。
- 正常系では `reset -> copy -> brlyt update -> brlan update -> encode -> cleanup -> move` の順で呼ばれる。

方針:

- 実ファイル全体を処理するE2Eにはしない。
- `load_color_settings_from_json`、`confirm_apply_colors`、`list_layout_json_files`、`encode_layout_json_files` などを `monkeypatch` で差し替える。
- 呼び出し順はリストにイベント名を追加して検証する。

完了条件:

- mainの早期returnと主要順序が保証されている。
- 外部アセットやwuj5なしで実行できる。

## フェーズ8: 実アセット依存テストを整理する

優先度: 低から中

対象:

- `Assets/BRLYT`
- `Assets/BRLAN`

方針:

- 単体テストとして必須にするケースと、実データ回帰として任意にするケースを分ける。
- 実アセット依存は `pytest.mark.integration` を付ける。
- CIで常時実行するかは、アセットのサイズと安定性を見て決める。

追加するテスト:

- 代表的なBRLYTファイルで `apply_tev_colors` が `None` にならない。
- 代表的なBRLANファイルで `update_tev_colors` が対象キーを更新する。
- 実アセット内の `.json` が `read_layout_json` で読み込める。

完了条件:

- 実アセットが無い環境でもユニットテストは通る。
- 実アセットありの環境では追加の回帰テストを走らせられる。

## 作業順

推奨順は以下です。

1. `test_json_io.py` を追加する。
2. `test_encode.py` を追加する。
3. `test_cleanup.py` に `remove_json_files` と上書きケースを追加する。
4. `test_brlan.py` に成分別・例外ルールのケースを追加する。
5. `test_brlyt.py` に複数ブロック・対象外ブロックのケースを追加する。
6. `test_i18n.py` を追加する。
7. `test_main_flow.py` を追加する。
8. 実アセット依存テストを `integration/` または marker で整理する。

## 各フェーズの完了チェック

各フェーズ完了時に以下を確認します。

```powershell
pytest
```

必要に応じて以下も実行します。

```powershell
ruff check .
```

完了時の基準:

- 既存テストがすべて通る。
- 新規テストが実アセットなしで skip されない。
- `tmp_path` 外へファイルを書かない。
- 外部変換器を必要としない。
- テスト名から何を守っているか分かる。

## 判断メモ

テスト追加中に実装の挙動が曖昧な箇所を見つけた場合は、先に仕様を決めます。

例:

- 壊れた `kind` を持つBRLANデータは無視するのか、例外にするのか。
- `.json5` 入力を今後も正式対応として残すのか、互換扱いにするのか。
- 実アセット依存テストをCI必須にするのか、任意実行にするのか。

この判断を曖昧にしたままテストを書くと、テストが仕様ではなく現在の偶然の挙動を固定してしまうため、ケース追加前に決めます。
