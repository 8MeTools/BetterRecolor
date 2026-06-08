---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "BetterRecolor"
  text: "Say goodbye to editing each color one by one!"
  tagline: Google Colab でもローカル環境でも、JSON / JSON5 化した BRLYT・BRLAN を編集して再生成できます。
  actions:
    - theme: brand
      text: 使い方を見る
      link: '/getting-started'
    - theme: alt
      text: GitHub
      link: https://github.com/8MeTools/BetterRecolor

features:
  - title: 色設定を一括管理
    details: color_config.json に指定した色を読み込み、BRLYT 側のプリセット色と BRLAN 側の縁取り色へ反映します。
  - title: Colab で実行可能
    details: Python 環境を手元に用意しなくても、ブラウザ上でセットアップから出力のダウンロードまで進められます。
  - title: ローカル実行にも対応
    details: Python 3.11 以上の環境があれば、手元の Assets/BRLYT と Assets/BRLAN を使って繰り返し処理できます。
  - title: 出力後の作業も明確
    details: 生成された Output を元のアセットへ反映し、Wiimms SZS Tool で再パックしてゲーム内で確認します。
---