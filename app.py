import os
import requests
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

COLAB_TRANSCRIBE_URL = "https://a339-34-16-236-206.ngrok-free.app"

@app.route('/transcribe', methods=['GET'])
def transcribe():
    video_url = request.args.get('url')
    video_id = video_url.split("v=")[-1]

    try:
        # Try fetching YouTube subtitles first
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t["text"] for t in transcript])
        return jsonify({"transcript": full_transcript})

    except:
        # If no subtitles, send request to Google Colab for Whisper AI transcription
        colab_response = requests.get(f"{COLAB_TRANSCRIBE_URL}?url={video_url}")
        return colab_response.json()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
