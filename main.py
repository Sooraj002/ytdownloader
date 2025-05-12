import yt_dlp

url = input("Enter the YouTube video URL: ").strip()

ydl_opts = {
    'format': 'best',
    'outtmpl': './output/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
