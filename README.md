# VideoFetch

VideoFetch downloads a YouTube video in a selected quality.

## Requirements

- Python
- Node.js, used by `yt-dlp` for YouTube JavaScript challenge support
- FFmpeg, used to combine video and audio into an MP4

Node.js and FFmpeg must be available on your system `PATH`.

## First-time setup

Open a terminal in the project folder and create a virtual environment:

```sh
python -m venv .venv
```

Activate it using the command for your operating system:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS or Linux
source .venv/bin/activate
```

Install the Python packages listed in `requirements.txt`:

```sh
python -m pip install -r requirements.txt
```

The virtual environment keeps this project's Python packages isolated from other projects. Activate it again whenever you open a new terminal to work on VideoFetch.

## Run the program

With the virtual environment activated, run this from the project folder:

```sh
python -m videofetch
```

The program will ask for:

1. The YouTube video URL
2. A folder name to create inside your `Downloads` folder (the first letter is capitalized)
3. The video quality
4. The output file name

The downloaded MP4 is saved in `Downloads/<FolderName>`. If a download is interrupted, run the program again and use the same file name to resume when a partial download is available.

## Project structure

- `videofetch/__init__.py` marks `videofetch` as a Python package and exposes the CLI function for imports. `videofetch/__main__.py` uses that package to start the program with `python -m videofetch`.
- `videofetch/__main__.py` starts the command-line program when you run `python -m videofetch`.
- `videofetch/cli.py` handles prompts and coordinates the download.
- `videofetch/quality.py` selects available video and audio formats.
- `videofetch/youtube.py` configures `yt-dlp` and performs extraction and downloads.
