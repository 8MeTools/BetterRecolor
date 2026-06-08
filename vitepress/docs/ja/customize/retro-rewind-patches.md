# Patchesシステムについて

最終更新日: 2026年5月18日

このページでは、Retro Rewind の `Patches` システムについて、UI ファイルを扱う上で必要になる基本的な考え方をまとめます。

::: info
このページは [Tockdom Wiki の Patches](https://wiki.tockdom.com/wiki/Patches) をもとにした補足資料です。最新仕様は元ページを確認してください。
:::

## 概要

`Patches` は、ゲーム内で読み込まれるファイルを外部ファイルで上書きする仕組みです。ユーザーが用意したファイルが存在する場合はそれを読み込み、存在しない場合はパックに同梱されているファイルを読み込みます。

従来の My Stuff に近い用途で使えますが、`.szs` 全体を置き換えるだけでなく、アーカイブ内部の一部ファイルだけを置き換えることもできます。

実装の参考:

- [LooseArchiveOverrides.cpp](https://github.com/Retro-Rewind-Team/rr-pulsar/blob/main/PulsarEngine/IO/LooseArchiveOverrides.cpp)
- [LooseBRSAROverrides.cpp](https://github.com/Retro-Rewind-Team/rr-pulsar/blob/main/PulsarEngine/Sound/LooseBRSAROverrides.cpp)

## できること

`Patches` では、主に次の上書き方式を利用できます。

| 方式 | 概要 |
| --- | --- |
| ファイル単位のオーバーライド | ゲームが要求するファイルを、外部の単体ファイルで置き換える |
| `.szs` 内サブファイルのオーバーライド | `.szs` 内の `.brlyt`、`.brlan`、`.tpl` などを置換、追加、削除する |
| `revo_kart.brsar` 内の音声ファイルのオーバーライド | `.brwsd`、`.brbnk`、`.brseq` などを File ID で置き換える |
| 差分アーカイブ | 複数のパッチファイルを 1 つの U8 / SZS アーカイブにまとめる |

## ファイル単位のオーバーライド

ファイル全体を置き換える場合は、編集したファイルを `Patches` フォルダに置き、上書きしたいファイルと同じ名前にします。

例:

```text
beginner_course.szs
n_Circuit32_n.brstm
n_Circuit32_f.brstm
```

ゲームが対象ファイルを読み込むとき、`Patches` にある同名ファイルが代わりに使用されます。

この方式は、完成済みの `.szs` や `.brstm` をそのまま差し替えたい場合に向いています。

::: warning
ファイル単位のオーバーライドは、基本的にファイル名で判定されます。ゲーム内に同名ファイルが複数ある場合、意図しない場所にも影響する可能性があります。
:::

## `.szs` 内サブファイルを置き換える

`.szs` 内の `.brlyt` や `.brlan` などを単体ファイルで置き換える場合は、次の命名規則を使用します。

```text
[Folder1][Folder2]filename.originalFormat.ArchiveTag
```

| 名前 | 内容 |
| --- | --- |
| `Folder1` | `.szs` 直下のフォルダ名。例: `bg`、`button`、`control` |
| `Folder2` | `Folder1` の中のフォルダ名。例: `anim`、`blyt`、`ctrl`、`timg` |
| `filename` | 置き換えるファイル名。例: `common_w004_menu` |
| `originalFormat` | 置き換えるファイルの拡張子。例: `.brlan`、`.brlyt`、`.tpl` |
| `ArchiveTag` | 対象 `.szs` のファイル名から拡張子を除いたもの。例: `menusingle` |

`ArchiveTag` の大文字と小文字は区別されません。たとえば `MenuSingle.szs` は `menusingle` と指定できます。

### フォルダを指定しない例

```text
common_w004_menu.brlyt.menusingle
```

この場合、`MenuSingle.szs` 内にある同名の `common_w004_menu.brlyt` がすべて置き換え対象になります。

例:

- `MenuSingle.szs/button/blyt/common_w004_menu.brlyt`
- `MenuSingle.szs/message_window/blyt/common_w004_menu.brlyt`

同名ファイルをまとめて置き換えたい場合は便利ですが、意図しない変更を起こす可能性があります。

### フォルダを指定する例

```text
[button][blyt]common_w004_menu.brlyt.menusingle
```

この場合、置き換え対象は `MenuSingle.szs/button/blyt/common_w004_menu.brlyt` に絞られます。

UI 系ファイルに限らず、内部ファイルパスと `ArchiveTag` が分かっていれば、他の `.szs` に対しても同じ考え方で指定できます。

## `.szs` 内にファイルを追加する

ファイルを追加する場合も、置き換えと同じ命名規則を使います。

```text
[Folder1][Folder2]filename.originalFormat.ArchiveTag
```

例として、`MenuSingle.szs` の `button/blyt` に `hogehoge.brlyt` を追加する場合は次のようにします。

```text
[button][blyt]hogehoge.brlyt.menusingle
```

追加先の親ディレクトリは、対象アーカイブ内に存在している必要があります。

## `.szs` 内のファイルを削除する

削除する場合は、拡張子の後ろに `.delete` を追加します。

```text
[Folder1][Folder2]filename.originalFormat.delete.ArchiveTag
```

例:

```text
[button][blyt]common_w004_menu.brlyt.delete.menusingle
```

フォルダを指定しない場合、アーカイブ内の同名ファイルがすべて削除対象になります。

```text
common_w004_menu.brlyt.delete.menusingle
```

::: warning
追加や削除を行う場合、メモリ上でアーカイブを再構築する必要があります。単純な置き換えより負荷が高くなる点に注意してください。
:::

## 差分アーカイブを使用する

複数のサブファイルをまとめて置き換える場合は、差分アーカイブを使うと管理しやすくなります。

命名規則:

```text
ModName.ArchiveTag.szs
```

| 名前 | 内容 |
| --- | --- |
| `ModName` | 任意の名前 |
| `ArchiveTag` | 対象 `.szs` のファイル名から拡張子を除いたもの |

例:

```text
MyMenuPack.menusingle.szs
```

このアーカイブ内に次のような構造があるとします。

```text
MyMenuPack.menusingle.szs
└── bg
    └── timg
        └── tt_obi_check_000.tpl
```

これは、次の単体パッチと同じ意味になります。

```text
[bg][timg]tt_obi_check_000.tpl.menusingle
```

差分アーカイブは、通常の U8 アーカイブまたは Yaz0 圧縮された `.szs` である必要があります。

### 優先順位

複数の差分アーカイブが同じ内部ファイルを対象にしている場合、ファイル名に数値の接頭辞を付けることで優先順位を制御できます。数値が小さいほど優先されます。

```text
001.MyMenuPack.menusingle.szs
010.MyMenuPack2.menusingle.szs
```

## BRSAR 内のファイルを置き換える

`revo_kart.brsar` 内部のファイルは、BRSAR の File ID によって置き換えられます。

基本形式:

```text
FileId.extension
```

ラベル付き形式:

```text
FileId.label.extension
```

対応拡張子:

- `.brwsd` または `.rwsd`
- `.brbnk` または `.rbnk`
- `.brseq` または `.rseq`

例:

```text
123.brwsd
123.menu_click.brwsd
456.brbnk
789.brseq
```

File ID は `0` から `1023` の範囲である必要があります。

## 方式の選び方

| 方式 | 向いているケース |
| --- | --- |
| ファイル単位のオーバーライド | 完成済みの `.szs` や `.brstm` をそのまま差し替える場合 |
| `.szs` 内サブファイルのオーバーライド | 大きなアーカイブの一部ファイルだけを変更する場合 |
| 差分アーカイブ | 複数のサブファイルをまとめて管理したい場合 |
| BRSAR オーバーライド | `revo_kart.brsar` 内の効果音、シーケンス、バンクを差し替える場合 |

## 制限事項と注意点

- フルファイル置き換えは、ファイル名のみで判定される場合があります。
- タグ付きアーカイブメンバーオーバーライドとフルファイルオーバーライドには、それぞれインデックス上限があります。
- BRSAR オーバーライドは File ID `0` から `1023` を使用します。
- 内部アーカイブパッチは、圧縮された `.szs` の読み込み時に適用されます。
- ファイル名や内部パスが間違っている場合、パッチは一致しません。

内部アーカイブパッチのサイズが大きすぎる場合、Dolphin のログに次のようなメッセージが出ることがあります。

```text
[Pulsar] Loose override repack allocation failed for 'SZSName': old=0x0 new=0x0 growth=0xSize source-heap growth capped.
```

この場合は、差分アーカイブではなくファイル単位のオーバーライドを検討してください。

