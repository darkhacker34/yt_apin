from flask import Flask, request, Response
from yt_dlp import YoutubeDL
import requests

app = Flask(__name__)

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400

    ydl_opts = {
        'format': 'best',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_url = info['url']

    def generate():
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    app.run()
