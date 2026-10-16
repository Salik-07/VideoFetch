# VideoFetch

VideoFetch downloads a YouTube video in a selected quality.

## Requirements

- Python
- Node.js, used by `yt-dlp` for YouTube JavaScript challenge support
- FFmpeg, used to combine video and audio into an MP4

Node.js and FFmpeg must be available on your system `PATH`.

## First-time setup

Open PowerShell in the project folder. Create the virtual environment and install the Python packages:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `requirements.txt` file specifies the `yt-dlp` package and its default dependencies. The virtual environment keeps these Python packages isolated for this project.

## Run the program

From this folder, run:

```powershell
.\.venv\Scripts\python.exe -m videofetch
```

The program will ask for:

1. The YouTube video URL
2. A folder name to create inside your `Downloads` folder (the first letter is capitalized)
3. The video quality
4. The output file name

The downloaded MP4 is saved in `Downloads\<FolderName>`. If a download is interrupted, run the program again and use the same file name to resume when a partial download is available.

## Project structure

- `videofetch/__init__.py` marks `videofetch` as a Python package.
- `videofetch/__main__.py` starts the command-line program with `python -m videofetch`.
- `videofetch/cli.py` handles prompts and coordinates the download.
- `videofetch/quality.py` selects available video and audio formats.
- `videofetch/youtube.py` configures `yt-dlp` and performs extraction and downloads.
