import yt_dlp

def select_quality():
    print("Select the video quality:")
    print("1. Best available (highest quality)")
    print("2. 1080p")
    print("3. 720p")
    print("4. Audio only (best audio)")
    print("5. Lowest quality")

    choice = input("Enter the number corresponding to your choice: ").strip()

    if choice == '1':
        return 'best'
    elif choice == '2':
        return 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif choice == '3':
        return 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif choice == '4':
        return 'bestaudio'
    elif choice == '5':
        return 'worst'
    else:
        print("Invalid choice, defaulting to best quality.")
        return 'best'

url = input("Enter the YouTube playlist or video URL: ").strip()

selected_quality = select_quality()

ydl_opts = {
    'format': selected_quality,
    'outtmpl': './output/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
    'ignoreerrors': True,
    'noplaylist': False,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
