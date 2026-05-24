# ButtonTextReColorizer JSONカラー設定 実装フロー

本書は、対話入力ベースだったカラー指定を JSON 読み込み方式へ移行し、実行前確認（Y/N）を追加するための実装フローをまとめたものです。

---

## 1. 目的

- 実行中にカラーコードを入力し直す手間をなくす
- 入力ミス時の `Ctrl+C` 再実行を減らす
- 実行前に最終確認できるようにする

---

## 2. JSON配置方針

推奨はプロジェクト直下です。

- 例: `color_config.json`
- 理由: `main.py` から相対パスで扱いやすく、CLI利用時に説明しやすい

複数プリセット運用をする場合は、将来的に `configs/colors/*.json` へ拡張します。

---

## 3. JSONスキーマ

最低限、以下を保持します。

- `presets`: BRLYT向けプリセット（white/black）
- `outline`: BRLAN向け縁取り色（free/select）

```json
{
  "presets": {
    "fuchi_pattern2": { "white": "#000000", "black": "#FFFFFF" },
    "color_base2": { "white": "#434343", "black": "#434343" },
    "color_yajirushi": { "white": "#C8C8C8", "black": "#FFFFFF" },
    "ability_graph2": { "white": "#434343", "black": "#000000" },
    "black_pt00": { "white": "#434343", "black": "#434343" }
  },
  "outline": {
    "free": "#282828",
    "select": "#787878"
  }
}
```

注意:

- HEXは `#RRGGBB` 形式のみ許可
- 依存プリセット（`color_base2 -> black_base2/pikapika`, `black_pt00 -> black_pt01`）はコード側で自動伝播

---

## 4. 実装ステップ

### Step 1: `btrc/config.py` にデフォルトJSONパスを追加

- `COLOR_CONFIG_PATH = BASE_DIR / "color_config.json"`
- 呼び出し側で未指定時の既定値として利用

### Step 2: `btrc/colors.py` にJSON読み込み処理を追加

追加関数例:

- `load_color_settings_from_json(path)`
  - JSON読み込み
  - 必須キー検証
  - HEX検証
  - `color_presets` を更新
  - 依存プリセットを伝播
  - 返却値:
    - `color_map`（既存 `run_color_input_flow()` と同じ構造）
    - `text_free_colors`（フリー状態のテキスト色＋縁取り色のタプル）
    - `text_select_colors`（選択状態のテキスト色＋縁取り色のタプル）

- `print_loaded_color_preview(color_map, text_free_colors, text_select_colors)`
  - 実行前プレビュー表示
  - 既存 `print_preset()` を流用
  
- `confirm_apply_colors()`
  - `Y/N` を受け付ける
  - `Y` なら `True`、それ以外は `False`

### Step 3: `main.py` の入力フローをJSONベースへ置換

現状:

- `run_color_input_flow()` で対話入力
- `get_outline_color_from_user()` で縁取り入力

変更後:

1. JSONパスを受け付ける（空欄ならデフォルト）
2. JSON読み込み
3. カラープレビュー表示
4. `Y/N` 確認
5. `Y` のみ処理継続、`N` は終了

### Step 4: i18n文言を追加

対象:

- `btrc/i18n/message.ja.yml`
- `btrc/i18n/message.en.yml`

追加キー例:

- `prompt_color_json_path`
- `color_json_load_success`
- `color_json_load_failed`
- `section_loaded_color_preview`
- `prompt_confirm_apply`
- `operation_cancelled`

### Step 5: READMEに運用手順を追記

- JSONの配置場所
- JSON例
- 実行時のY/N確認仕様
- エラー時の対処（必須キー不足、HEX不正、ファイル未検出）

---

## 5. エラー処理方針

- ファイル未存在: 明示メッセージを表示して終了
- JSON構文不正: 例外内容を含めて表示して終了
- スキーマ不正: どのキーが不足しているか表示して終了
- HEX不正: 問題のキー名と値を表示して終了

---

## 6. 受け入れ条件

- JSONから色設定を読み込める
- 実行前に全カラーが一覧表示される
- `Y/N` 確認が機能する
- `N` で処理が止まる
- 既存のBRLYT/BRLAN更新処理に影響がない

---

## 7. テスト観点

新規テスト候補:

- 正常JSONで `color_map` が正しく生成される
- `outline.free/select` がRGB変換される
- 依存プリセットが伝播される
- 必須キー不足で例外になる
- 不正HEXで例外になる
- 確認入力 `Y/N` の分岐が正しい

既存テスト（`test_brlan.py`, `test_brlyt.py`）は更新処理本体の回帰確認として併用する。

---

## 8. 導入後の運用イメージ

1. `color_config.json` を編集
2. `python main.py` 実行
3. プレビューを確認
4. `Y` で適用
5. 出力を `Output` で確認

この方式により、設定は再利用可能になり、実行時の入力ミスによるやり直しコストを大幅に削減できます。
