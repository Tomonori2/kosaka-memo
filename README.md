# 高坂先生のメモAI 🤖

音声をAIで自動文字起こし＆要約するWebアプリです。ピポパポ！

サーバー不要の**完全クライアント側アプリ**。あなたのGroqキーで、ブラウザから直接AIを呼び出します。

## デモ

👉 **https://tomonori2.github.io/kosaka-memo/**

> 初回だけ、自分のGroq APIキーの登録が必要です（下記参照）。

## 機能

- 🎙️ **録音** — ブラウザで直接マイク録音
- 🎵 **音声ファイルアップロード** — MP3 / M4A / WAV / WEBM など（25MBまで）
- 📝 **文字起こし** — Whisper（Groq API）で高精度に変換
- 💫 **要約** — 要点を箇条書きでまとめる
- 📋 **会議メモ整理** — 議題・決定事項・次のアクションに自動整理
- 📱 **PWA対応** — スマホのホーム画面にインストール可能

## 使い方

1. **STEP 0** で自分のGroq APIキーを登録（最初の1回だけ）
2. マイクボタンで録音 or 音声ファイルを選ぶ
3. 自動で文字起こし
4. 「要約する」か「会議メモに整理」を押す

## 🔑 APIキーについて

このアプリは **BYOK（Bring Your Own Key／自分の鍵を持参）** 方式です。

- Groq APIキーは https://console.groq.com/keys で**無料**取得できます
- 入力したキーは **あなたの端末のブラウザ（localStorage）にだけ**保存されます
- キーは **Groq以外のどのサーバーにも送信されません**（このアプリにはサーバーがありません）
- 料金は各自のGroqアカウントにかかります

## 🔒 セキュリティ設計

- サーバーを持たないため、第三者がキーや音声データを預かることがありません
- 通信はすべて HTTPS（GitHub Pages）＋ Groqへの直接通信のみ
- キーはブラウザ内のみ。別の端末・ブラウザには共有されません

## 使用技術

| 技術 | 用途 |
|------|------|
| HTML / JavaScript | フロントエンド（サーバーレス） |
| Groq API (Whisper) | 音声文字起こし |
| Groq API (LLaMA 3.3) | 要約・会議メモ整理 |
| GitHub Pages | ホスティング |
| PWA | スマホアプリ化 |

## ローカルで動かす

ビルド不要。静的ファイルを配信するだけです。

```bash
git clone https://github.com/tomonori2/kosaka-memo.git
cd kosaka-memo
python -m http.server 5050
```

→ http://localhost:5050 にアクセス（マイク録音にはhttps か localhost が必要です）

## GitHub Pagesで公開する

1. GitHubリポジトリの **Settings → Pages** を開く
2. **Source** を `Deploy from a branch` にする
3. Branch を `main`（フォルダは `/root`）に設定して Save
4. 数分後 `https://<ユーザー名>.github.io/kosaka-memo/` で公開されます
