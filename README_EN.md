# Music Format Converter 🎵

A modern, user-friendly music format converter with a graphical interface, supporting batch conversion of entire folders and single file conversion.

## ✨ Features

- **Modern GUI**: Dark theme with intuitive interface
- **Batch Conversion**: Convert entire folders of music files at once
- **Single File Conversion**: Convert individual music files
- **Multiple Formats**: Support for MP3, WAV, FLAC, AAC, OGG, M4A
- **Real-time Progress**: Visual progress bar and status updates
- **Detailed Logging**: Operation history and error reporting
- **Thread Safe**: Background processing without UI freezing

## 📋 Supported Formats

### Input Formats
- MP3
- WAV
- FLAC
- AAC
- M4A
- OGG
- WMA
- APE
- TTA

### Output Formats
- MP3
- WAV
- FLAC
- AAC
- OGG
- M4A

## 🚀 Quick Start

### Prerequisites

1. **Install FFmpeg** (Required)
   - **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html), extract and add to system PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

2. **Verify FFmpeg installation**
   ```bash
   ffmpeg -version
   ```

### Installation & Running

#### Method 1: Using Batch Script (Recommended)
```bash
# Double-click run.bat or start.bat
```

#### Method 2: Manual Execution
```bash
cd music_converter
# Activate virtual environment (if needed)
.venv\Scripts\activate
# Run the program
python main.py
```

## 📖 Usage Guide

### 1. Convert Single File
1. Click "选择音乐文件" (Select Music File)
2. Choose one or more music files
3. Select output format from dropdown
4. Click "开始转换" (Start Conversion)

### 2. Convert Entire Folder
1. Click "选择音乐文件夹" (Select Music Folder)
2. Choose folder containing music files
3. Select output format
4. (Optional) Set custom output directory
5. Click "开始转换" (Start Conversion)

### 3. Output Directory
- **Default**: Creates `converted` subfolder in original directory
- **Custom**: Specify any directory path
- **Single File**: Saved in original file's directory

## 🛠️ Technology Stack

- **GUI Framework**: PyQt6
- **Audio Processing**: pydub + ffmpeg-python
- **Package Management**: uv
- **Python Version**: 3.12+

## 📁 Project Structure

```
music_converter/
├── main.py              # Main application entry
├── converter.py         # Core conversion logic
├── ui.py               # GUI interface
├── requirements.txt    # Dependencies
├── README.md          # Documentation (Chinese)
├── README_EN.md       # Documentation (English)
├── run.bat            # Windows startup script
├── start.bat          # Simplified startup script
├── test.py            # Functionality test
├── .gitignore         # Git ignore rules
└── 快速开始.md        # Quick start guide (Chinese)
```

## ⚙️ Dependencies

```txt
PyQt6>=6.5.0
pydub>=0.25.1
ffmpeg-python>=0.2.0
```

Install using uv:
```bash
uv pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Q: "Cannot find ffmpeg" error
**A**: Ensure FFmpeg is installed and added to system PATH

### Q: Program won't start
**A**: Check if dependencies are installed: `uv pip install -r requirements.txt`

### Q: Conversion fails
**A**: Check if the input file is corrupted or in a supported format

### Q: Slow conversion
**A**: Large files take time to process, this is normal

### Q: UI shows "Recursive repaint detected" errors
**A**: This has been fixed in the latest version. Update to the newest code.

## 📝 Version History

### v1.0.0
- ✨ Basic functionality complete
- ✨ Modern dark theme interface
- ✨ Batch and single file conversion
- ✨ Real-time progress display
- ✨ Detailed operation logs
- ✨ Thread-safe UI updates

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is open source and free to use.

## 🙏 Credits

Developed by AI Assistant with modern GUI design and thread-safe architecture.

---

**Enjoy your music conversion!** 🎉
