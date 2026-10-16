"""Video and audio format selection helpers."""

QUALITY_TIERS = [
    (480, "480p"),
    (720, "720p"),
    (1080, "1080p"),
    (1440, "1440p"),
    (2160, "4K (2160p)"),
]


def format_size(size_bytes):
    if not size_bytes:
        return "size unknown"
    size_mb = size_bytes / (1024 * 1024)
    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    return f"{size_mb:.1f} MB"


def _estimated_size(format_info):
    return format_info.get("filesize") or format_info.get("filesize_approx") or 0


def pick_best_video(formats, max_height=None):
    candidates = [
        format_info
        for format_info in formats
        if format_info.get("height")
        and format_info.get("vcodec") not in (None, "none")
        and (max_height is None or format_info["height"] <= max_height)
    ]
    if not candidates:
        return None

    mp4_candidates = [format_info for format_info in candidates if format_info.get("ext") == "mp4"]
    pool = mp4_candidates or candidates
    return max(
        pool,
        key=lambda format_info: (
            format_info.get("height") or 0,
            _estimated_size(format_info),
        ),
    )


def pick_best_audio(formats):
    candidates = [
        format_info
        for format_info in formats
        if format_info.get("acodec") not in (None, "none")
        and format_info.get("vcodec") in (None, "none")
    ]
    if not candidates:
        return None

    m4a_candidates = [format_info for format_info in candidates if format_info.get("ext") == "m4a"]
    pool = m4a_candidates or candidates
    return max(pool, key=lambda format_info: format_info.get("abr") or 0)


def build_quality_options(formats):
    audio = pick_best_audio(formats)
    audio_size = _estimated_size(audio) if audio else 0
    max_height = max(
        (
            format_info.get("height") or 0
            for format_info in formats
            if format_info.get("vcodec") not in (None, "none")
        ),
        default=0,
    )

    options = []
    seen_heights = set()

    for height, label in QUALITY_TIERS:
        if height > max_height:
            continue

        video = pick_best_video(formats, height)
        if not video or video["height"] in seen_heights:
            continue

        seen_heights.add(video["height"])
        options.append(
            {
                "label": label,
                "height": video["height"],
                "size": _estimated_size(video) + audio_size,
                "format": (
                    f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/"
                    f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
                ),
            }
        )

    best_video = pick_best_video(formats)
    if best_video and best_video["height"] not in seen_heights:
        options.append(
            {
                "label": f"Best available ({best_video['height']}p)",
                "height": best_video["height"],
                "size": _estimated_size(best_video) + audio_size,
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            }
        )

    return options
