import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import threading
import sys
import shutil

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x450")
        self.root.configure(padx=20, pady=20)

        # Setup FFmpeg path
        self.setup_ffmpeg()

        # URL Entry
        url_frame = ttk.LabelFrame(root, text="URL", padding="10")
        url_frame.pack(fill="x", pady=(0, 10))
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill="x", padx=5)

        # Download Path
        path_frame = ttk.LabelFrame(root, text="Download Location", padding="10")
        path_frame.pack(fill="x", pady=(0, 10))
        
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=45)
        path_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_btn.pack(side="right")

        # Quality Selection
        quality_frame = ttk.LabelFrame(root, text="Quality", padding="10")
        quality_frame.pack(fill="x", pady=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        qualities = [
            ("Best Quality", "bestvideo+bestaudio/best"),
            ("1080p", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("720p", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("480p", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("Audio Only (Best)", "bestaudio")
        ]
        
        for text, value in qualities:
            ttk.Radiobutton(quality_frame, text=text, value=value, 
                           variable=self.quality_var).pack(anchor="w")

        # Format Selection
        format_frame = ttk.LabelFrame(root, text="Format", padding="10")
        format_frame.pack(fill="x", pady=(0, 10))
        
        self.format_var = tk.StringVar(value="video")
        ttk.Radiobutton(format_frame, text="Video (MP4)", value="video", 
                       variable=self.format_var).pack(side="left", padx=20)
        ttk.Radiobutton(format_frame, text="Audio (MP3)", value="audio", 
                       variable=self.format_var).pack(side="left")

        # Progress
        progress_frame = ttk.LabelFrame(root, text="Progress", padding="10")
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Ready to download...")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(fill="x")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=(5, 0))

        # Download Button
        self.download_btn = ttk.Button(root, text="Download", command=self.start_download)
        self.download_btn.pack(pady=10)

    def get_base_path(self):
        """Get the base path for the application"""
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle
            return sys._MEIPASS
        else:
            # If the application is run from a Python interpreter
            return os.path.dirname(os.path.abspath(__file__))

    def setup_ffmpeg(self):
        """Setup FFmpeg path for the application"""
        base_path = self.get_base_path()
        ffmpeg_dir = os.path.join(base_path, 'ffmpeg')
        
        if not os.path.exists(ffmpeg_dir):
            os.makedirs(ffmpeg_dir, exist_ok=True)
        
        # Set FFmpeg path for yt-dlp
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)

    def download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        try:
            output_path = self.path_var.get()
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            if self.format_var.get() == 'audio':
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'extractaudio': True,
                    'audioformat': 'mp3',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'progress_hooks': [self.progress_hook],
                }
            else:
                ydl_opts = {
                    'format': self.quality_var.get(),
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'progress_hooks': [self.progress_hook],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.progress_var.set("Download completed!")
            self.progress_bar['value'] = 100
            messagebox.showinfo("Success", f"Download completed successfully!\nSaved in: {output_path}")

        except Exception as e:
            self.progress_var.set("Error occurred during download")
            messagebox.showerror("Error", str(e))

        finally:
            self.download_btn.configure(state="normal")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = d['_percent_str']
                percent = float(percent.replace('%', ''))
                self.progress_bar['value'] = percent
                self.progress_var.set(f"Downloading: {d['_percent_str']}")
            except:
                self.progress_bar['value'] = 0
                self.progress_var.set("Downloading...")
        elif d['status'] == 'finished':
            self.progress_var.set("Processing downloaded files...")
            self.progress_bar['value'] = 100

    def start_download(self):
        self.download_btn.configure(state="disabled")
        self.progress_var.set("Starting download...")
        self.progress_bar['value'] = 0
        threading.Thread(target=self.download, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
