---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "BetterRecolor"
  text: "ひとつひとつの色編集に別れを告げましょう。"
  tagline: Google Colab でもローカル環境でも、JSON化した BRLYT・BRLAN を編集して再生成できます。
  actions:
    - theme: brand
      text: 使い方を見る
      link: '/ja/getting-started'
    - theme: alt
      text: Colabで試す
      link: https://colab.research.google.com/github/8MeTools/BetterRecolor/blob/main/BetterRecolor.ipynb
    - theme: alt
      text: GitHub
      link: https://github.com/8MeTools/BetterRecolor

features:
  - title: 色設定を一括管理
    details: color_config.json に指定した色を読み込み、BRLYT 側のプリセット色と BRLAN 側の縁取り色へ反映します。
  - title: Colab で実行可能
    details: Python 環境を手元に用意しなくても、ブラウザ上でセットアップから出力のダウンロードまで進められます。
  - title: ローカル実行にも対応
    details: Python 3.11 以上の環境があれば、お手元の環境で繰り返しの処理が可能です。
  - title: 出力後の作業も明確
    details: 生成されたサブアセットを元のアセットへ反映し、Wiimms SZS Tool で再パックしてゲーム内で確認します。
---