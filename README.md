# YouTube Downloader

A simple GUI application to download YouTube videos and playlists with quality options. The application comes with FFmpeg bundled, so no additional installation is required.

## Download

You can download the ready-to-use executable from:
[YouTubeDownloader.exe](dist/YouTubeDownloader.exe)

## Features

- Easy-to-use graphical interface
- Download YouTube videos and playlists
- Multiple quality options:
  - Best Quality (highest available)
  - 1080p
  - 720p
  - 480p
  - Audio Only (best audio quality)
- Format options:
  - Video (MP4)
  - Audio (MP3)
- Progress bar showing download status
- Choose your own download location
- No FFmpeg installation required (bundled with the application)

## How to Use

1. **Launch the Application**
   - Simply double-click `YouTubeDownloader.exe`
   - No installation needed

2. **Download a Video**
   - Copy a YouTube URL (video or playlist)
   - Paste it into the URL field
   - Choose your preferred download location (defaults to your Downloads folder)
   - Select quality (Best, 1080p, 720p, 480p, or Audio Only)
   - Choose format (Video MP4 or Audio MP3)
   - Click "Download"
   - Wait for the download to complete

3. **Download Location**
   - Click "Browse" to choose where to save your downloads
   - The application remembers your last selected location

## For Developers

If you want to run from source or modify the code:

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Git Bash):
     ```bash
     source venv/Scripts/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```

### Building the Executable

To create your own executable:
```bash
pyinstaller youtube_downloader.spec
```
The executable will be created in the `dist` folder.

## Troubleshooting

1. **Video Download Failed**
   - Check your internet connection
   - Try a different quality option
   - Verify the video is available in your region

2. **No Audio in Video**
   - This shouldn't happen as the application automatically merges audio and video
   - If it does occur, try downloading with "Best Quality" option

3. **Application Won't Start**
   - Make sure you're running on Windows
   - Try running as administrator
   - Check your antivirus isn't blocking the application

## Note

This application is for personal use only. Please respect YouTube's terms of service and copyright laws.
