"""yt-dlp integration for extracting video details and downloading media."""

from pathlib import Path

import yt_dlp


BASE_YDL_OPTIONS = {
    "quiet": True,
    "no_warnings": True,
    # Retry transient network and file access errors, and resume partial files.
    "continuedl": True,
    "retries": 20,
    "fragment_retries": 20,
    "file_access_retries": 5,
    "extractor_retries": 5,
    "socket_timeout": 60,
    # YouTube uses JavaScript challenges for full format access.
    "js_runtimes": {"node": {}},
    "remote_components": ["ejs:github"],
}


class YouTubeDownloadError(Exception):
    """A user-facing error raised while communicating with yt-dlp."""


def extract_video_info(url):
    try:
        with yt_dlp.YoutubeDL(BASE_YDL_OPTIONS) as downloader:
            return downloader.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as exc:
        raise YouTubeDownloadError(f"Could not read video information: {exc}") from exc


def download_video(url, quality, output_file):
    options = {
        **BASE_YDL_OPTIONS,
        "outtmpl": str(Path(output_file)),
        "format": quality["format"],
        "merge_output_format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download([url])
    except yt_dlp.utils.DownloadError as exc:
        raise YouTubeDownloadError(
            f"Download stopped: {exc}\n"
            "Check your internet connection and free disk space, then run the program "
            "again with the same filename to resume the partial download."
        ) from exc
    except OSError as exc:
        raise YouTubeDownloadError(
            f"File or disk error: {exc}\n"
            "Check free disk space and folder permissions, then run the program "
            "again with the same filename to resume the partial download."
        ) from exc
