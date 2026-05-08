import os
import subprocess


def create_thumbnail(video_path):
    """
    Creates a JPG thumbnail from the first second of the uploaded video.
    """

    base, _ = os.path.splitext(video_path)
    thumbnail_path = f"{base}.jpg"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-ss",
            "00:00:01",
            "-vframes",
            "1",
            "-update",
            "1",
            thumbnail_path,
        ],
        check=True,
    )

    return thumbnail_path


def convert_to_hls_quality(video_path, quality_name, height):
    """
    Converts a video into one HLS quality level.
    """

    base, _ = os.path.splitext(video_path)
    output_dir = f"{base}_{quality_name}_hls"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "index.m3u8")
    segment_path = os.path.join(output_dir, "index%d.ts")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-vf",
            f"scale=-2:{height}",
            "-c:v",
            "libx264",
            "-profile:v",
            "main",
            "-crf",
            "20",
            "-sc_threshold",
            "0",
            "-g",
            "48",
            "-keyint_min",
            "48",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-start_number",
            "0",
            "-hls_time",
            "4",
            "-hls_playlist_type",
            "vod",
            "-hls_segment_filename",
            segment_path,
            "-f",
            "hls",
            output_path,
        ],
        check=True,
    )

    return output_path


def convert_to_hls(video_path):
    """
    Converts the uploaded video into all supported HLS quality levels.
    """

    return {
        "480p": convert_to_hls_quality(video_path, "480p", 480),
        #"720p": convert_to_hls_quality(video_path, "720p", 720),
        #"1080p": convert_to_hls_quality(video_path, "1080p", 1080),
    }