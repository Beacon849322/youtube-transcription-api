import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcribe', methods=['GET'])
def transcribe():
    video_url = request.args.get('url')
    video_id = video_url.split("v=")[-1]

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t["text"] for t in transcript])
        return jsonify({"transcript": full_transcript})

    except Exception as e:
        return jsonify({"error": "No subtitles found. Use Google Colab for audio processing."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
