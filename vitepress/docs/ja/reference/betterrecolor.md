# BetterRecolor とは

最終更新日: 2026年4月3日

BetterRecolor は、ゲーム内に表示されるボタンやテキストの色をまとめて変更するためのツールです。

手作業で UI ファイルを編集する場合、変更対象のファイルを探し、複数の `BRLYT` / `BRLAN` を編集し、反映漏れがないか確認する必要があります。BetterRecolor はこの作業を `color_config.json` に集約し、まとめて処理できるようにします。

## できること

- ボタンやテキストの色を一括変更する
- `BRLYT` 側の色設定をまとめて反映する
- `BRLAN` 側の縁取り色をまとめて反映する
- Google Colab またはローカル環境で実行する
- 出力されたファイルを `Output` にまとめる

## Google Colab を使う利点

Colab を使うと、ローカルに Python 環境を用意しなくても BetterRecolor を実行できます。

| 利点 | 内容 |
| --- | --- |
| 実行環境に依存しにくい | クラウド上の割り当てられたマシンで処理するため、手元の PC 環境差を受けにくくなります。 |
| 環境構築が不要 | ブラウザ上でセルを実行するだけで、依存関係のインストールから処理まで進められます。 |

Python やゲーム内部ファイルの構造に詳しくない場合は、まず Colab 版から使うことを推奨します。

## 基本的な入出力

BetterRecolor の入力・設定・出力は次のように分かれています。

| 種類 | 場所 |
| --- | --- |
| 入力 | `Assets/BRLYT` と `Assets/BRLAN` |
| 色設定 | `color_config.json` |
| 出力 | `Output` |

詳しい実行手順は [クイックスタート](/ja/getting-started) を参照してください。

## 色設定の考え方

`color_config.json` では、主に次の項目を編集します。

| 項目 | 内容 |
| --- | --- |
| `presets` | BRLYT 側で使用する色 |
| `outline.free` | 通常時の BRLAN 側の縁取り色 |
| `outline.select` | 選択時の BRLAN 側の縁取り色 |

色は `#RRGGBB` 形式で指定します。

## Switch Toolbox で色を確認する

`color_config.json` の `white` や `black` などの項目は、Switch Toolbox で確認できる Pane の色と対応しています。Switch Toolbox で表示を確認しながら色を決め、その値を `color_config.json` に反映すると調整しやすくなります。

例として、`MenuSingle.szs` には次のような Pane があります。

| Pane Name | File Name |
| --- | --- |
| `fuchi_pattern2` (`fuchi_pattern`) | `./button/blyt/common_w004_menu.brlyt` |
| `color_base2` (`color_base`) | `./button/blyt/common_w004_menu.brlyt` |
| `color_yajirushi` | `./button/blyt/common_w016_yajirushi_left.brlyt` |
| `ability_graph2` (`ability_graph`) | `./control/blyt/common_w099_machine_ability.brlyt` |
| `black_pt00` (`black_parts_t_00`) | `./control/blyt/common_w027_chara_name.brlyt` |

::: tip
バニラのファイルで探す場合は、括弧内の Pane Name を探してください。
:::

Switch Toolbox で `MenuSingle.szs` を開き、対象 Pane の色を確認します。変更したい色が決まったら、対応する `color_config.json` の値を編集して BetterRecolor を実行します。

