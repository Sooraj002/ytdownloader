import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import threading
import sys
import shutil
import darkdetect

class ModernYouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x700")
        self.root.minsize(800, 650)
        
        # Configure window icon and properties
        self.root.configure(bg='#1a1a1a')
        
        # Variables
        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.quality_var = tk.StringVar(value="bestvideo+bestaudio/best")
        self.format_var = tk.StringVar(value="video")
        self.progress_var = tk.StringVar(value="Ready to download")
        
        # Setup modern theme
        self.setup_modern_theme()
        
        # Create main interface
        self.create_interface()
        
        # Setup FFmpeg
        self.setup_ffmpeg()
        
        # Make window responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def setup_modern_theme(self):
        """Setup modern dark theme with custom styling"""
        style = ttk.Style()
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1a1a1a',      # Main background
            'bg_secondary': '#2d2d2d',    # Card backgrounds
            'bg_tertiary': '#404040',     # Input backgrounds
            'accent': '#00d4ff',          # Primary accent (cyan)
            'accent_hover': '#00bfea',    # Accent hover
            'success': '#00ff88',         # Success green
            'warning': '#ffaa00',         # Warning orange
            'error': '#ff4444',           # Error red
            'text_primary': '#ffffff',    # Primary text
            'text_secondary': '#b3b3b3',  # Secondary text
            'border': '#404040',          # Border color
        }
        
        # Configure styles
        style.theme_use('clam')
        
        # Main frame style
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='solid')
        
        # Label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 28, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 11))
        
        style.configure('Header.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Body.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.configure('Caption.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9))
        
        # Entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_tertiary'],
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       insertcolor=self.colors['accent'],
                       font=('Segoe UI', 11))
        
        style.map('Modern.TEntry',
                 focuscolor=[(('focus',), self.colors['accent'])])
        
        # Button styles
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='#000000',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent'])])
        
        style.configure('Secondary.TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       borderwidth=1,
                       focuscolor='none')
        
        style.map('Secondary.TButton',
                 background=[('active', '#505050')])
        
        # Radiobutton styles
        style.configure('Modern.TRadiobutton',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        style.map('Modern.TRadiobutton',
                 background=[('active', self.colors['bg_secondary'])])
        
        # Progressbar style
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'],
                       thickness=8)

    def create_interface(self):
        """Create the main interface"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        main_frame.columnconfigure(0, weight=1)
        
        # Header section
        self.create_header(main_frame)
        
        # URL input section
        self.create_url_section(main_frame)
        
        # Download path section
        self.create_path_section(main_frame)
        
        # Options section
        self.create_options_section(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Download button
        self.create_download_section(main_frame)

    def create_header(self, parent):
        """Create header with title and subtitle"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 40))
        
        title = ttk.Label(header_frame, text="YouTube Downloader Pro", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header_frame, 
                           text="Download videos and audio from YouTube in high quality", 
                           style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))

    def create_url_section(self, parent):
        """Create URL input section"""
        url_frame = self.create_card_frame(parent, "Video URL")
        url_frame.pack(fill='x', pady=(0, 20))
        
        # URL entry with placeholder effect
        self.url_entry = ttk.Entry(url_frame, 
                                  textvariable=self.url_var,
                                  style='Modern.TEntry',
                                  font=('Segoe UI', 12))
        self.url_entry.pack(fill='x', padx=20, pady=15)
        
        # Placeholder text
        self.url_placeholder = "Paste YouTube URL here..."
        self.setup_placeholder(self.url_entry, self.url_placeholder, self.url_var)

    def create_path_section(self, parent):
        """Create download path section"""
        path_frame = self.create_card_frame(parent, "Download Location")
        path_frame.pack(fill='x', pady=(0, 20))
        
        path_container = tk.Frame(path_frame, bg=self.colors['bg_secondary'])
        path_container.pack(fill='x', padx=20, pady=15)
        
        # Use pack for path entry and button
        self.path_entry = ttk.Entry(path_container,
                                   textvariable=self.path_var,
                                   style='Modern.TEntry',
                                   font=('Segoe UI', 11))
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        browse_btn = ttk.Button(path_container,
                               text="Browse",
                               command=self.browse_path,
                               style='Secondary.TButton')
        browse_btn.pack(side='right')

    def create_options_section(self, parent):
        """Create options section with quality and format"""
        options_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        options_container.pack(fill='x', pady=(0, 20))
        
        # Create a horizontal container for the two frames
        frames_container = tk.Frame(options_container, bg=self.colors['bg_primary'])
        frames_container.pack(fill='x')
        
        # Quality options
        quality_frame = self.create_card_frame(frames_container, "Quality Settings")
        quality_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_quality_options(quality_frame)
        
        # Format options
        format_frame = self.create_card_frame(frames_container, "Output Format")
        format_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        self.create_format_options(format_frame)

    def create_quality_options(self, parent):
        """Create quality selection options"""
        qualities = [
            ("🎯 Best Available", "bestvideo+bestaudio/best"),
            ("🎬 1080p HD", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("📺 720p HD", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("📱 480p", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("🎵 Audio Only", "bestaudio")
        ]
        
        for i, (text, value) in enumerate(qualities):
            rb = ttk.Radiobutton(parent,
                               text=text,
                               value=value,
                               variable=self.quality_var,
                               style='Modern.TRadiobutton')
            rb.pack(anchor='w', padx=20, pady=(5 if i == 0 else 2, 5 if i == len(qualities)-1 else 2))

    def create_format_options(self, parent):
        """Create format selection options"""
        formats = [
            ("🎥 Video (MP4)", "video"),
            ("🎧 Audio (MP3)", "audio")
        ]
        
        for i, (text, value) in enumerate(formats):
            rb = ttk.Radiobutton(parent,
                               text=text,
                               value=value,
                               variable=self.format_var,
                               style='Modern.TRadiobutton')
            rb.pack(anchor='w', padx=20, pady=(15 if i == 0 else 5, 15 if i == len(formats)-1 else 5))

    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = self.create_card_frame(parent, "Download Progress")
        progress_frame.pack(fill='x', pady=(0, 30))
        
        # Progress text
        self.progress_label = ttk.Label(progress_frame,
                                       textvariable=self.progress_var,
                                       style='Body.TLabel')
        self.progress_label.pack(padx=20, pady=(15, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          mode='determinate',
                                          style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x', padx=20, pady=(0, 15))

    def create_download_section(self, parent):
        """Create download button section"""
        download_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        download_container.pack(fill='x')
        
        self.download_btn = ttk.Button(download_container,
                                      text="⬇ Start Download",
                                      command=self.start_download,
                                      style='Accent.TButton')
        self.download_btn.pack(pady=10)
        
        # Configure button size
        self.download_btn.configure(width=20)

    def create_card_frame(self, parent, title):
        """Create a card-style frame with title"""
        container = tk.Frame(parent, bg=self.colors['bg_primary'])
        container.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(container, text=title, style='Header.TLabel')
        title_label.pack(anchor='w', pady=(0, 8))
        
        # Card frame
        card = ttk.Frame(container, style='Card.TFrame')
        card.pack(fill='both', expand=True)
        
        return card

    def setup_placeholder(self, entry, placeholder_text, text_var):
        """Setup placeholder text for entry widget"""
        def on_focus_in(event):
            if text_var.get() == placeholder_text:
                text_var.set('')
                entry.config(foreground=self.colors['text_primary'])

        def on_focus_out(event):
            if text_var.get() == '':
                text_var.set(placeholder_text)
                entry.config(foreground=self.colors['text_secondary'])

        # Set initial placeholder
        text_var.set(placeholder_text)
        entry.config(foreground=self.colors['text_secondary'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def get_base_path(self):
        """Get the base path for the application"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def setup_ffmpeg(self):
        """Setup FFmpeg path for the application"""
        try:
            base_path = self.get_base_path()
            ffmpeg_dir = os.path.join(base_path, 'ffmpeg')
            
            if os.path.exists(os.path.join(ffmpeg_dir, 'ffmpeg.exe')):
                os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
                return
            
            if getattr(sys, '_MEIPASS', None):
                meipass_ffmpeg = os.path.join(sys._MEIPASS, 'ffmpeg')
                if os.path.exists(os.path.join(meipass_ffmpeg, 'ffmpeg.exe')):
                    os.environ["PATH"] = meipass_ffmpeg + os.pathsep + os.environ.get("PATH", "")
                    return
            
        except Exception as e:
            print(f"FFmpeg setup warning: {e}")

    def browse_path(self):
        """Browse for download directory"""
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)

    def validate_inputs(self):
        """Validate user inputs"""
        url = self.url_var.get().strip()
        if not url or url == self.url_placeholder:
            messagebox.showerror("Invalid Input", "Please enter a valid YouTube URL")
            return False
        
        if not os.path.exists(self.path_var.get()):
            try:
                os.makedirs(self.path_var.get())
            except Exception as e:
                messagebox.showerror("Path Error", f"Cannot create download directory:\n{e}")
                return False
        
        return True

    def download(self):
        """Main download function"""
        if not self.validate_inputs():
            return
        
        url = self.url_var.get().strip()
        
        try:
            output_path = self.path_var.get()
            
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

            # Success
            self.progress_var.set("✅ Download completed successfully!")
            self.progress_bar['value'] = 100
            
            # Show success message
            result = messagebox.showinfo("Download Complete", 
                                       f"Download completed successfully!\n\nSaved to: {output_path}\n\nWould you like to open the folder?")
            
            # Optionally open the folder
            try:
                if sys.platform == "win32":
                    os.startfile(output_path)
                elif sys.platform == "darwin":
                    os.system(f"open '{output_path}'")
                else:
                    os.system(f"xdg-open '{output_path}'")
            except:
                pass

        except Exception as e:
            self.progress_var.set("❌ Download failed")
            self.progress_bar['value'] = 0
            messagebox.showerror("Download Error", f"An error occurred:\n\n{str(e)}")

        finally:
            self.download_btn.configure(state="normal", text="⬇ Start Download")

    def progress_hook(self, d):
        """Handle download progress updates"""
        if d['status'] == 'downloading':
            try:
                if '_percent_str' in d:
                    percent_str = d['_percent_str'].strip()
                    percent = float(percent_str.replace('%', ''))
                    self.progress_bar['value'] = percent
                    
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    
                    self.progress_var.set(f"⬇ Downloading {percent_str} • {speed} • ETA: {eta}")
                else:
                    self.progress_var.set("⬇ Downloading...")
                    
            except (ValueError, KeyError):
                self.progress_var.set("⬇ Downloading...")
                
        elif d['status'] == 'finished':
            self.progress_var.set("🔄 Processing downloaded file...")
            self.progress_bar['value'] = 95

    def start_download(self):
        """Start the download process"""
        if not self.validate_inputs():
            return
            
        self.download_btn.configure(state="disabled", text="⏳ Downloading...")
        self.progress_var.set("🚀 Initializing download...")
        self.progress_bar['value'] = 0
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.download, daemon=True)
        download_thread.start()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set window properties
    root.state('zoomed') if sys.platform == "win32" else root.attributes('-zoomed', True)
    
    app = ModernYouTubeDownloader(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()