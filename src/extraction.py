from pydub import AudioSegment


def extraction(video_path: str, audio_path: str, audio_format="wav"):
    audio_segment = AudioSegment.from_file(video_path)
    audio_segment = audio_segment.set_channels(1)
    audio_segment = audio_segment.set_frame_rate(16_000)
    path = audio_segment.export(audio_path, audio_format)
    return path
