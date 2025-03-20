from flask import Flask, request, Response
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError
import requests

app = Flask(__name__)

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400
    if not url.startswith(('http://', 'https://')):
        return "Invalid URL: Must start with http:// or https://", 400

    ydl_opts = {
        'format': 'best',
        'cookiefile': '/app/cookies.txt',  # Path inside the container
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
    except (DownloadError, ExtractorError) as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            return "This video requires authentication. Cookies may be expired or invalid.", 403
        elif "Too Many Requests" in error_msg:
            return "Rate limit exceeded by YouTube. Please try again later.", 429
        return f"Error processing URL: {error_msg}", 400
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

    def generate():
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    app.run()
