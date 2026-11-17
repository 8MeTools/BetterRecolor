# Retro Rewind v6.13.5以降 タイトル画面でクラッシュした場合の対処法

最終更新日: 2026年11月17日

お久しぶりです。BetterRecolor管理人です。

**Retro Rewind v6.13.5**以降にアプデしたユーザーから、「タイトル画面の読込時にクラッシュする」という相談を受け、問題を解消できたのでこちらにまとめます。

対象となるのは、**ボタンカラーをbrlyt側で定義できるように編集したSZSを使用しているユーザー**です(以下、Recolor系統と呼びます)。ゲーム内設定のカラーに依存しないようにボタンカラーが変わっているならば、十中八九この問題の対象です。

## 今回の解決策
対象のBRLYTファイルに`fuchi_pattern`という名前のPane名が存在しない場合は、ダミー用にPane名を新規に作成する。

### 対象のファイル
- /button/blyt/common_w067_title_large_3parts.brlyt
- /button/blyt/common_w067_title_large_2parts.brlyt
- /button/blyt/common_w067_title_large_1parts.brlyt

詳しい情報については後述していきます。

## いつからこの問題が起きたのか

2026/11/07に、RRが**v6.13.5**にアップデートされました。Discordでアナウンスされたチェンジログに、以下の記述がありました。これが原因のようですね。

```text
- Modified the button colors to readd the button animations.
```

このアップデートにより、一部のMy Stuffユーザーはタイトル画面でライセンスをセレクトした直後にクラッシュするようになりました。

## 原因となっているコード
gitのコミット履歴を見ていくと、RRのアップデート前に以下のようなコードが追加されていました。
```cpp
void UpdateTitleButtonColors(Pages::MainMenu *page) {
    // The Channel frame is not loaded on Dolphin. Use the page's loaded count.
    for (u32 i = 0; i < page->internControlCount; ++i) {
        LayoutUIControl &frame = page->buttonTitles[i];
        for (u32 j = 0; j < frame.childrenGroup.controlCount; ++j) {
            PushButton *button = frame.childrenGroup.GetControl<PushButton>(j);
            nw4r::lyt::Picture *pattern = static_cast<nw4r::lyt::Picture *>(button->fuchi_pattern);
            // Remove the title layout's yellow tint without changing animation alpha.
            for (u32 k = 0; k < 4; ++k) {
                pattern->vertexColours[k].r = 255;
                pattern->vertexColours[k].g = 255;
                pattern->vertexColours[k].b = 255;
            }
        }
    }
}
kmBranch(0x80851108, UpdateTitleButtonColors);
```

引用: [Fix title button UI colors - rr-pulsar](https://github.com/Retro-Rewind-Team/rr-pulsar/commit/c67b16b18d62bd27193a29de890ddb0482a85c13)

C++のコードが読めなくても問題はありません。関数の名前からも分かる通り、タイトル画面のボタンカラーを更新する役割を担っています。

具体的に見てみましょう。 対象となるPane名は、`fuchi_pattern`です。`pattern->vertexColours[k].r = 255`のような実装から、頂点カラーの値を255にしています。RGBで同様の処理をすることから、頂点カラーをHTMLカラーコードで表すと`#FFFFFF`(白色)になります。

## brlyt側の構成を見る
![純正brlytのfuchi_patternの頂点カラーが黄色（#FFFF00FF）になっている](/img/fix-title-screen-crash/01.png)

これは純正のTitle.szsに含まれる`/button/blyt/common_w067_title_large_2parts.brlyt`をSwitch Toolboxで開いた際のプレビューです。`fuchi_pattern`のPaneを選択してVertex Colorの項目を確認すると、`#FFFF00FF`(黄色)になっています。最後の`FF`はアルファ値(透明度)です。

先述のC++コードは、この黄色を白色に変更するための役割を担っていることになります。つまり、変更前は`#FFFF00FF`だったのが、コード適用後は`#FFFFFFFF`という状態になります。変更後のイメージは以下を見てください。

![fuchi_patternの頂点カラーを白色にした場合のプレビュー](/img/fix-title-screen-crash/02.png)

ピンク色の部分は気になると思いますが、今回は無視して大丈夫です。純正のbrlytでは、ボタンカラーがゲーム側で決定されるため、ピンク色の部分は実際には表示されないからです。

::: details 黄色を白色に変更しなければならない理由を考察
Retro Rewindではゲーム内でHUDカラーを設定できますが、ここで設定したカラーがタイトルのボタンに限っては適切に反映されません。例えば、HUDカラーをブルーに設定した場合、タイトルのボタンカラーは青色ではなく緑色のように見えます。これは、brlyt側の黄ばみと青色が混ざっているためです。見た目上の問題を解消するため、RR側ではC++コードで黄色を白色に変更していると考えられます。あくまで憶測ですが...。
:::

## Recolor系統でクラッシュする原因
Recolor系統では、Pane名が`fuchi_pattern`という名前から変更されているためです。例えばBTRCでは`fuchi_pattern2`という名前に変更することで、ゲームシステム側からではなく、SZS単位でカラーを適用できるようにしています。他の方も、このようなPane名を変更するやり方を採用していると思います。

先述のC++のコードでは、`fuchi_pattern`というPane名が存在しないと適切な処理ができずにクラッシュしてしまいます。

## 解決策: `fuchi_pattern`をダミーで作成する
裏を返せば、`fuchi_pattern`というPane名がとにかくあれば、クラッシュする問題は防ぐことができます。

SZS単位でカラーを適用する以上、`fuchi_pattern2`を消すわけにはいきません。brlytに新規に`fuchi_pattern`という名前でPaneを作成してあげましょう。

今回はGUIアプリケーションである Switch Toolboxを使用してBRLYTを編集するやり方を掲載します。

作業フォルダには、Title.szsだけでなく、展開したフォルダ(Title.d)を置いておくことをおすすめします。

![エクスプローラーのファイル一覧を表示した画面](/img/fix-title-screen-crash/10.png)

### 1. SZSをSwitch Toolboxで開く
SZSファイルはSwitch Toolboxで開くことができます。開けたら、`button`→`blyt`に進み、対象となる`.brlyt`ファイルをダブルクリックで開きます。

![Switch ToolboxでSZSを開き、button/blyt内のbrlytを表示した画面](/img/fix-title-screen-crash/03.png)

今回、編集対象となる`.brlyt`ファイルは以下の通りです。
- /button/blyt/common_w067_title_large_3parts.brlyt
- /button/blyt/common_w067_title_large_2parts.brlyt
- /button/blyt/common_w067_title_large_1parts.brlyt

### 2. Paneを新規に作成する

プレビューが表示された後、プレビューの格子線上で右クリックして、**Create Pane(Paneの新規作成)** → **Picture Pane**を選択してください。
![プレビュー上の右クリックメニューからCreate Pane → Picture Paneを選ぶ](/img/fix-title-screen-crash/04.png)

白色の四角が新しく表示されていると思います。これでPaneが作成できました。デフォルトでは`P_pict`という名前でPaneが作成されていると思います。

![P_pictという名前でPicture Paneが作成された状態](/img/fix-title-screen-crash/05.png)

### 3. Paneの名前/座標を変更する
`P_pict`を選択して、左側の**Pane**を選択します。
Pane infoのすぐ下にある**Name**の部分を変更することで、Pane名を変更することができます。今回は、`fuchi_pattern`という名前に変更してください。

![PaneタブでName欄とTranslateの座標を確認する](/img/fix-title-screen-crash/06.png)

次に、座標を変更します。ここは正直やらなくてもよいですが、合わせておきましょう。

名前を変更したところの少し下にある**Translate**を探してください。上記の画像では、座標がX: -100/Y: -37になっていますが、この値は人によって異なります。XもYも座標は0に変更しておいてください。中央に四角が来ると思います。

### 4. Paneの透明度を変更する
今度は**Picture Pane**タブに移動して、Vertex Color(頂点カラー)の透明度を変更します。
![Picture PaneタブのVertex Colors欄](/img/fix-title-screen-crash/07.png)

**ALL**の部分を選択すると、カラーパレットが出現します。透明度を0にしてください。

![Color DialogでAを0にし、Hexが FFFFFF00 になった状態](/img/fix-title-screen-crash/08.png)

プレビューから白色の四角が見えなくなりました。RR側のコードではアルファ値に変更を加えないため、ゲーム内でも白色の四角は表示されません。

### 5. brlytを保存する
左上の**File**→**Save As**でbrlytを保存することができます。展開したSZSファイルのbrlytを置き換える形で上書き保存してください。

![File → Save Asでbrlytを保存する](/img/fix-title-screen-crash/09.png)

::: warning
SZSの展開・圧縮の操作はここでは解説しません。
:::
今回は`common_w067_title_large_3parts.brlyt`を編集したので、他のファイルも同じ手順でPaneを作成してください。

## ゲームで確認する
変更したbrlytが含まれるSZSを圧縮したら、ゲーム内で問題なく動作するか確認してください。クラッシュせずに進めたら成功です。お疲れ様でした。
