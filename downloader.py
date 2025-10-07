from yt_dlp import YoutubeDL
import os

def download_video(url, output_dir="downloads"):
    """
    Download a single YouTube video as best quality MP4.
    Returns the file path.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True  # single video only
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename
        
