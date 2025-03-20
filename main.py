from flask import Flask, request, Response
from yt_dlp import YoutubeDL
import requests

app = Flask(__name__)

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400
    
    # Basic URL validation (optional: improve with regex if needed)
    if not url.startswith(('http://', 'https://')):
        return "Invalid URL: Must start with http:// or https://", 400

    ydl_opts = {
        'format': 'best',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
    except Exception as e:
        return f"Error processing URL: {str(e)}", 400

    def generate():
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    app.run()
