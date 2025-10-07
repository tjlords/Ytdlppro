import yt_dlp
import os

DOWNLOAD_PATH = "./downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def download_video(url, quality="bestvideo+bestaudio"):
    ydl_opts = {
        "format": quality,
        "outtmpl": os.path.join(DOWNLOAD_PATH, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": False,  # Download playlist if URL is playlist
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if "entries" in info_dict:  # playlist
            file_path = []
            for entry in info_dict["entries"]:
                filename = ydl.prepare_filename(entry)
                file_path.append(filename)
            return file_path[0]  # For simplicity, return first video path
        else:
            return ydl.prepare_filename(info_dict)
