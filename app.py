from flask import Flask, render_template, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os
import uuid
from urllib.error import HTTPError
import re
import time

app = Flask(__name__)

# Configure upload folder
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/process-url', methods=['POST'])
def process_url():
    try:
        data = request.json
        url = data.get('url')
        format_type = data.get('format', 'mp3')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        unique_filename = f"{uuid.uuid4().hex}"
        output_path = os.path.join(DOWNLOAD_FOLDER, unique_filename)

        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'extract_audio': True,
                'audio_format': 'mp3',
                # Removed postprocessors to avoid FFmpeg dependency
            }
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
            }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')

        return jsonify({
            'success': True,
            'title': title,
            'filename': unique_filename,
            'format': format_type
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    match = re.match(youtube_regex, url)
    return bool(match)

@app.route('/download-file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Determine the file extension based on the requested format
        extension = 'mp3' if '.mp3' in filename else 'mp4'
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"download.{extension}",
            mimetype=f'audio/{extension}' if extension == 'mp3' else f'video/{extension}'
        )
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

# Cleanup function for downloaded files
def cleanup_downloads():
    try:
        current_time = time.time()
        for filename in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            # Remove files older than 1 hour
            if os.path.getmtime(file_path) < current_time - 3600:
                try:
                    os.remove(file_path)
                except:
                    continue
    except Exception as e:
        print(f"Cleanup error: {str(e)}")

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(debug=True) 