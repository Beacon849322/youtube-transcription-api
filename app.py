from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
import os
import yt_dlp

app = Flask(__name__)

def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.mp3',
        'cookiefile': 'cookies.txt'  # This will use cookies for authentication
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def transcribe_audio():
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    return result["text"]

@app.route('/transcribe', methods=['GET'])
def transcribe():
    video_url = request.args.get('url')
    video_id = video_url.split("v=")[-1]

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([t["text"] for t in transcript])
        return jsonify({"transcript": full_transcript})

    except:
        download_audio(video_url)
        text = transcribe_audio()
        os.remove("audio.mp3")  # Clean up the file
        return jsonify({"transcript": text})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
