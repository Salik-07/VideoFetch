"""Command-line prompts and application flow for VideoFetch."""

import shutil
from pathlib import Path

from videofetch.quality import build_quality_options, format_size
from videofetch.youtube import YouTubeDownloadError, download_video, extract_video_info


def prompt_for_url():
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        raise SystemExit("YouTube URL cannot be empty.")
    return url


def prompt_for_folder_name():
    folder_name = input("Enter a folder name inside Downloads: ").strip()
    if not folder_name:
        raise SystemExit("Folder name cannot be empty.")
    if folder_name in {".", ".."} or any(
        character in folder_name for character in '<>:"/\\|?*'
    ):
        raise SystemExit("Folder name contains characters that are not allowed.")
    return folder_name[0].upper() + folder_name[1:]


def choose_quality(options):
    print("\nAvailable qualities:")
    for index, option in enumerate(options, start=1):
        print(
            f"  {index}. {option['label']} "
            f"({option['height']}p) - {format_size(option['size'])}"
        )

    while True:
        choice = input("\nSelect quality (enter number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"Please enter a number between 1 and {len(options)}.")


def prompt_for_filename():
    filename = input("\nEnter file name for the download: ").strip()
    if not filename:
        raise SystemExit("File name cannot be empty.")
    if not filename.lower().endswith(".mp4"):
        filename += ".mp4"
    return filename


def ensure_sufficient_disk_space(download_dir, estimated_size):
    if not estimated_size:
        return

    available_bytes = shutil.disk_usage(download_dir).free
    # Leave headroom because YouTube's file size estimates can be approximate.
    required_bytes = int(estimated_size * 1.1)
    if available_bytes < required_bytes:
        raise SystemExit(
            "Not enough free disk space for this download. "
            f"Estimated need: {format_size(required_bytes)}; "
            f"available: {format_size(available_bytes)}."
        )


def main():
    url = prompt_for_url()
    folder_name = prompt_for_folder_name()
    download_dir = Path.home() / "Downloads" / folder_name

    try:
        download_dir.mkdir(parents=True, exist_ok=True)
        video_info = extract_video_info(url)
    except YouTubeDownloadError as exc:
        raise SystemExit(str(exc)) from exc
    except OSError as exc:
        raise SystemExit(f"Could not prepare the download folder: {exc}") from exc

    quality_options = build_quality_options(video_info.get("formats", []))
    if not quality_options:
        raise SystemExit("No downloadable video formats found for this URL.")

    selected_quality = choose_quality(quality_options)
    output_file = download_dir / prompt_for_filename()

    try:
        ensure_sufficient_disk_space(download_dir, selected_quality["size"])
        download_video(url, selected_quality, output_file)
    except YouTubeDownloadError as exc:
        raise SystemExit(str(exc)) from exc
    except OSError as exc:
        raise SystemExit(
            f"File or disk error: {exc}\n"
            "Check free disk space and folder permissions, then run the program "
            "again with the same filename to resume the partial download."
        ) from exc

    print(
        f"\nDownloaded: {output_file}\n"
        f"Quality: {selected_quality['label']} ({selected_quality['height']}p)"
    )
