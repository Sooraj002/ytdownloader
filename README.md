# YouTube Downloader Pro

A modern, user-friendly YouTube video and audio downloader with a sleek dark-themed GUI built using Python and tkinter.

![YouTube Downloader Pro](screenshots/app.png)

## Features

- 🎥 Download YouTube videos in multiple quality options (Best, 1080p, 720p, 480p)
- 🎵 Extract audio in MP3 format
- 🎨 Modern dark theme UI with rounded corners
- 📊 Real-time download progress tracking
- 📂 Custom download location selection
- 🔄 Format conversion using FFmpeg
- ⚡ Asynchronous downloads
- 🖥️ Cross-platform compatibility

## Requirements

- Python 3.7+
- FFmpeg
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/youtube-downloader-pro.git
cd youtube-downloader-pro
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download and install FFmpeg:
   - Windows: Place FFmpeg executables in the `ffmpeg` folder
   - Linux/Mac: Install via package manager
     ```bash
     # Ubuntu/Debian
     sudo apt-get install ffmpeg
     
     # macOS
     brew install ffmpeg
     ```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter a YouTube URL
3. Select your preferred quality and format
4. Choose download location
5. Click "Start Download"

## Features in Detail

- **Quality Options**:
  - Best Available (maximum quality)
  - 1080p HD
  - 720p HD
  - 480p
  - Audio Only (MP3)

- **Format Options**:
  - Video (MP4)
  - Audio (MP3)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the YouTube download functionality
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- [FFmpeg](https://ffmpeg.org/) for media processing
