from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# APIキーは環境変数から読む（コードには絶対に書かない）
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def index():
    return send_from_directory(_BASE_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    """manifest.json・sw.js・robot.png などを配信（.envやコードは渡さない）"""
    if filename.startswith(".") or filename.endswith((".env", ".py")):
        return ("Not found", 404)
    return send_from_directory(_BASE_DIR, filename)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """音声ファイルをWhisperで文字起こしする"""
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "ファイルがありません"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"ok": False, "error": "ファイルが選ばれていません"}), 400

    # サイズ制限（25MB・Whisperの上限）
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > 25 * 1024 * 1024:
        return jsonify({"ok": False, "error": "ファイルが大きすぎます（25MBまで）"}), 400

    try:
        audio_data = file.read()
        transcription = client.audio.transcriptions.create(
            file=(file.filename, audio_data),
            model="whisper-large-v3",
            response_format="verbose_json",
            language="ja",
        )
        return jsonify({
            "ok": True,
            "text": transcription.text,
            "duration": getattr(transcription, "duration", None),
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# 要約モードごとのAIへの指示書
SUMMARY_PROMPTS = {
    "summary": (
        "あなたは福井県出身の癒し系ロボット『高坂先生』です。口癖は「ピポパポ！」。"
        "渡された文字起こしを、要点だけ分かりやすく箇条書きで要約してください。"
        "難しい言葉は使わず、最後に高坂先生らしいひとことを添えてください。"
    ),
    "meeting": (
        "あなたは会議の書記を担当する『高坂先生』です。"
        "渡された文字起こしを、次の見出しで整理してください:\n"
        "【議題】\n【主な発言・意見】\n【決定事項】\n【次にやること（担当・期限があれば）】\n"
        "発言が曖昧な部分は推測せず『不明』と書いてください。"
    ),
}


@app.route("/summarize", methods=["POST"])
def summarize():
    """文字起こしテキストをAIで要約 or 会議メモに整理する"""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    mode = data.get("mode", "summary")

    if not text:
        return jsonify({"ok": False, "error": "要約するテキストがありません"}), 400
    if mode not in SUMMARY_PROMPTS:
        mode = "summary"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SUMMARY_PROMPTS[mode]},
                {"role": "user", "content": text},
            ],
        )
        return jsonify({"ok": True, "result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
