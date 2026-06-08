# BTRCで変更したサブファイルを Patches を利用して適用する

最終更新日: 2026年5月19日

このページでは、BetterRecolor で生成したボタン・テキストカラーの変更を、Retro Rewind の `Patches` システムで適用する方法を説明します。

`Patches` システム自体の概要は、先に [Retro Rewind Patches](./retro-rewind-patches) を確認してください。

## 方針

BetterRecolor で生成される UI ファイルは数が多いため、すべてを単体ファイルとして `Patches` に置くと管理が難しくなります。

そのため、次の 2 つの方式を使い分けるのが現実的です。

| 方式 | 用途 |
| --- | --- |
| ファイル単位のオーバーライド | `MenuSingle.szs` や `Race.szs` など、既存の MKWii UI ファイルを大きく変更する場合 |
| 差分アーカイブ | `UIAssets.szs` や `RaceAssets.szs` など、Retro Rewind 側で追加された UI ファイルを扱う場合 |

::: tip
BetterRecolor の出力はファイル数が多いため、`[button][blyt]common_w004_menu.brlyt.menusingle` のような単体サブファイル指定を大量に作る方法は基本的に向きません。
:::

## BetterRecolor の出力

BetterRecolor の処理後、生成物は `Output` フォルダにまとめられます。

過去のバージョンでは `EditedBRLYT` と `EditedBRLAN` に分かれていましたが、現在は利用しやすさを優先して `Output` に統合されています。

出力には、次のようなフォルダが含まれます。

```text
Output/
├── MenuSingle.d/
├── Race.d/
├── UIAssets.d/
└── ...
```

`.d` フォルダは、SZS に再パックする前の展開済みフォルダです。

## 移植が必要なものを分ける

BetterRecolor の出力は、すべて同じ扱いにするのではなく、対象ファイルごとに扱いを分けます。

### 既存の MKWii UI ファイル

`MenuSingle.d` や `Race.d` など、既存の MKWii UI ファイルに対応するものは、必要に応じて `.szs` に再パックし、ファイル単位のオーバーライドとして `Patches` に置きます。

この方式は従来の My Stuff に近く、完成済みの `.szs` をそのまま置き換える形です。

### Retro Rewind 側の追加 UI ファイル

`UIAssets.d` や `ReplacedAssets.d` など、Retro Rewind 側で追加された UI ファイルは、差分アーカイブとして扱う方が適している場合があります。

BetterRecolor の出力で `RRUIAssets.d` のような名前になっている場合は、用途に応じて `UIAssets.d` にリネームしてから扱います。

## `.d` フォルダを SZS に圧縮する

Wiimms SZS Tool を使う場合、次のコマンドで `.d` フォルダを SZS に圧縮できます。

```sh
wszst c FileName.d -o
```

`-o` は上書き指定です。既に同名の SZS がある場合でも上書きして生成できます。

同じディレクトリ内の複数の `.d` フォルダをまとめて圧縮する場合は、次のように実行できます。

```sh
wszst c *.d -o
```

## `Patches` 用にファイル名を変更する

`Patches` で読み込ませる場合、ファイルの種類によって名前の付け方が変わります。

### 既存の SZS

`MenuSingle.szs` や `Race.szs` など、既存の SZS を完全に上書きする場合は、そのままの名前で `Patches` フォルダに置きます。

```text
Patches/
└── MenuSingle.szs
```

### Retro Rewind 側の追加 SZS

`UIAssets.szs` や `ReplacedAssets.szs` などを差分アーカイブとして扱う場合は、次の形式にします。

```text
yourmodname.uiassets.szs
yourmodname.replacedassets.szs
```

`yourmodname` は任意の英数字名に置き換えてください。

## 言語設定が英語以外の場合

UIAssets は、ゲーム側の言語設定によって読み込まれる差分名が変わる場合があります。

日本語設定で `UIAssets` の差分が読み込まれない場合は、`uiassets` の後ろに `_j` を付けます。

```text
yourmodname.uiassets_j.szs
```

## 作業例

BetterRecolor の `Output` を使う場合の流れは次の通りです。

1. BetterRecolor を実行して `Output` を生成する
2. 必要な `.d` フォルダを確認する
3. 既存 UI ファイルは `.szs` に圧縮する
4. Retro Rewind 側の追加 UI ファイルは用途に応じて差分アーカイブ名へ変更する
5. 生成した `.szs` を `Patches` フォルダへ配置する
6. ゲーム内で反映を確認する

## 使い分けの目安

| 対象 | 推奨 |
| --- | --- |
| `MenuSingle.szs` など既存 UI を大きく変更する場合 | ファイル単位のオーバーライド |
| `UIAssets.szs` など RR 側の追加 UI を変更する場合 | 差分アーカイブ |
| 数個の内部ファイルだけを変更する場合 | `.szs` 内サブファイルのオーバーライド |
| BetterRecolor の出力をまとめて適用する場合 | ファイル単位のオーバーライドと差分アーカイブの併用 |

BetterRecolor の出力は変更対象が多くなりやすいため、管理しやすい単位で SZS 化してから `Patches` に置く方法が扱いやすいです。

