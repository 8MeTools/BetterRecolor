import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Better Recolor Wiki",
  description: "An accessible UI editing tool for MKWii, powered by Google Colab and local envs.",
  srcExclude: ['temp/**'],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/getting-started' },
      { text: 'Reference', link: '/reference/' },
      { text: 'Try in Colab', link: 'https://colab.research.google.com/github/8MeTools/BetterRecolor/blob/main/BetterRecolor.ipynb' },
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Quick Start', link: '/getting-started' }
        ]
      },
      {
        text: 'Reference',
        items: [
          { text: 'Overview', link: '/reference/' },
          { text: 'What Is BetterRecolor?', link: '/reference/betterrecolor' },
          { text: 'Run on WSL2', link: '/reference/wsl2' }
        ]
      },
      {
        text: 'Customization',
        items: [
          { text: 'Overview', link: '/customize/' },
          { text: 'Retro Rewind Patches', link: '/customize/retro-rewind-patches' },
          { text: 'Apply with Patches', link: '/customize/betterrecolor-patches' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/8MeTools/BetterRecolor' }
    ]
  },
  locales: {
    root: {
      label: 'English',
      lang: 'en'
    },
    ja: {
      label: 'Japanese',
      lang: 'ja',
      link: '/ja/',
      themeConfig: {
        nav: [
          { text: 'ホーム', link: '/ja/' },
          { text: 'クイックスタート', link: '/ja/getting-started' },
          { text: 'リファレンス', link: '/ja/reference/' },
          { text: 'Colabで試す', link: 'https://colab.research.google.com/github/8MeTools/BetterRecolor/blob/main/BetterRecolor.ipynb' },
        ],
        sidebar: [
          {
            text: 'はじめに',
            items: [
              { text: 'クイックスタート', link: '/ja/getting-started' }
            ]
          },
          {
            text: 'リファレンス',
            items: [
              { text: '概要(リファレンス)', link: '/ja/reference/' },
              { text: 'BetterRecolor とは', link: '/ja/reference/betterrecolor' },
              { text: 'WSL2 で実行する', link: '/ja/reference/wsl2' },
            ]
          },
          {
            text: 'カスタマイズ',
            items: [
              { text: '概要(カスタマイズ)', link: '/ja/customize/' },
              { text: 'Patchesシステムについて', link: '/ja/customize/retro-rewind-patches' },
              { text: 'Patchesを利用して適用する', link: '/ja/customize/betterrecolor-patches' }
            ]
          }
        ]
      }
    },
  }
})
