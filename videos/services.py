# NEU: videos/services.py

import os
import subprocess


def create_thumbnail(video_path):
    base, _ = os.path.splitext(video_path)
    thumbnail_path = f"{base}.jpg"

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            "00:00:01",
            "-vframes",
            "1",
            thumbnail_path,
        ],
        check=True,
    )

    return thumbnail_path