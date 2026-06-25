# 高坂先生のメモAI 🤖

音声をAIで自動文字起こし＆要約するWebアプリです。ピポパポ！

## デモ

👉 **https://kosaka-memo.onrender.com**

> 無料サーバーのため、初回起動に30秒〜1分かかることがあります。

## 機能

- 🎙️ **録音** — ブラウザで直接マイク録音
- 🎵 **音声ファイルアップロード** — MP3 / M4A / WAV / WEBM など（25MBまで）
- 📝 **文字起こし** — Whisper（Groq API）で高精度に変換
- 💫 **要約** — 要点を箇条書きでまとめる
- 📋 **会議メモ整理** — 議題・決定事項・次のアクションに自動整理
- 📱 **PWA対応** — スマホのホーム画面にインストール可能

## 使い方

1. マイクボタンで録音 or 音声ファイルを選ぶ
2. 自動で文字起こし
3. 「要約する」か「会議メモに整理」を押す

## 使用技術

| 技術 | 用途 |
|------|------|
| Python / Flask | バックエンド |
| Groq API (Whisper) | 音声文字起こし |
| Groq API (LLaMA 3.3) | 要約・会議メモ整理 |
| Render | ホスティング |
| PWA | スマホアプリ化 |

## ローカルで動かす

```bash
git clone https://github.com/tomonori2/kosaka-memo.git
cd kosaka-memo
pip install -r requirements.txt
```

`.env` ファイルを作成：
```
GROQ_API_KEY=your_api_key_here
```

起動：
```bash
python app.py
```

→ http://localhost:5050 にアクセス

## APIキーの取得

Groq APIキーは https://console.groq.com で無料取得できます。
