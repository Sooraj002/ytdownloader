import yt_dlp

url = input("Enter the YouTube playlist or video URL: ").strip()

ydl_opts = {
    'format': 'best',
    'outtmpl': './output/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
    'ignoreerrors': True,  # Skip videos that fail to download
    'noplaylist': False    # Enable full playlist download
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
