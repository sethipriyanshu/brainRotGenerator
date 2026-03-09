import subprocess


# Use this if you need to trim longer videos from sample video
def trim_video(input_path, output_path, duration=10):
    command = [
        'ffmpeg',
        '-y',
        '-i', input_path,  # Input file
        '-t', str(duration),  # Duration to trim (in seconds)
        '-c', 'copy',  # Copy codec (no re-encoding)
        output_path  # Output file
    ]
    subprocess.run(command, check=True)


# Overlay TTS audio on the base video only.
# Your ffmpeg build does not include the 'subtitles' filter, so we skip
# burning in subtitles here and rely on the image overlays instead.
def add_subtitles_and_overlay_audio(video_path, audio_path, subtitles_path, output_path):
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,  # Input video file
        '-i', audio_path,  # Input audio file
        '-c:v', 'libx264',  # Video codec
        "-map", "0:v",
        "-map", "1:a",
        '-c:a', 'aac',  # Audio codec
        '-strict', 'experimental',  # Allow experimental codecs
        '-shortest',  # Match the shortest input duration
        output_path  # Output file
    ]
    subprocess.run(command, check=True)

trim_video('assets/subway.mp4','assets/trimed.mp4', duration = 120)