from yt_dlp import YoutubeDL
import os

def download_video(url, output_dir="downloads", quality="best"):
    """
    Download single video or playlist from YouTube.
    - url: YouTube URL
    - quality: 'best', '1080p', '720p', etc.
    Returns list of downloaded file paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best' if quality != "best" else 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': False,  # allow playlists
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True
    }

    downloaded_files = []
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Single video or playlist
        if 'entries' in info:
            for entry in info['entries']:
                if entry:
                    filepath = ydl.prepare_filename(entry)
                    downloaded_files.append(filepath)
        else:
            filepath = ydl.prepare_filename(info)
            downloaded_files.append(filepath)

    return downloaded_files
