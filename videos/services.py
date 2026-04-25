import os
import subprocess


def create_thumbnail(video_path):
    base, _ = os.path.splitext(video_path)
    thumbnail_path = f"{base}.jpg"

    subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-ss", "00:00:01",
            "-vframes", "1",
            "-update", "1",
            thumbnail_path,
        ],
        check=True,
    )

    return thumbnail_path


def convert_to_hls_quality(video_path, quality_name, height):
    base, _ = os.path.splitext(video_path)
    output_dir = f"{base}_{quality_name}_hls"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "index.m3u8")

    subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vf", f"scale=-2:{height}",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-start_number", "0",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls",
            output_path,
        ],
        check=True,
    )

    return output_path


def convert_to_hls(video_path):
    return {
        "480p": convert_to_hls_quality(video_path, "480p", 480),
        "720p": convert_to_hls_quality(video_path, "720p", 720),
        "1080p": convert_to_hls_quality(video_path, "1080p", 1080),
    }