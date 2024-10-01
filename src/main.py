from pathlib import Path

import streamlit as st

from environment import (
    VOSK_MODEL_SMALL_CN,
    VOSK_MODEL_SMALL_EN_US,
    VOSK_MODEL_SMALL_FR,
    VOSK_MODEL_SMALL_JA,
    VOSK_MODEL_SMALL_PT,
)
from extraction import extraction
from subtitling import subtitling
from transcription import transcription


def main() -> None:
    PATH = Path(".tmp")
    PATH.mkdir(exist_ok=True)

    st.set_page_config(
        page_title="Hihi",
        page_icon=":monkey:",
        menu_items={
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "# This is a header. This is an *extremely* cool app!",
        },
    )

    uploaded_file = st.file_uploader(
        label="Lorem, ipsum dolor.",
        type=["avi", "mkv", "mp4", "webm"],
        label_visibility="hidden",
    )

    if not uploaded_file:
        return None

    VIDEO_PATH = str(
        PATH.joinpath(f"{uploaded_file.file_id}{Path(uploaded_file.name).suffix}")
    )

    Path(VIDEO_PATH).write_bytes(uploaded_file.getbuffer())

    st.video(uploaded_file, format=uploaded_file.type)

    locale = st.selectbox("Language", options=["en", "fr", "ja", "pt", "zh"], index=3)
    button = st.button("Subtitle", type="primary", use_container_width=True)

    SRT_PATH = str(PATH.joinpath(f"{uploaded_file.file_id}.srt"))

    if not button and Path(SRT_PATH).exists():
        st.status("Subtitling complete.", state="complete")

        st.video(
            uploaded_file,
            format=uploaded_file.type,
            subtitles=SRT_PATH,
        )

        st.download_button(
            "Download subtitle",
            Path(SRT_PATH).read_bytes(),
            f"{uploaded_file.file_id}.srt",
            "application/octet-stream",
            use_container_width=True,
        )
    elif button:
        with st.status("Subtitling in progress...") as status:
            # 0
            status.update(label="[1/3] Audio extraction...")

            AUDIO_PATH = extraction(
                VIDEO_PATH, str(PATH.joinpath(f"{uploaded_file.file_id}.wav"))
            )

            # 1
            status.update(label="[2/3] Transcription...")
            if locale == "en":
                MODEL_PATH = VOSK_MODEL_SMALL_EN_US
            elif locale == "fr":
                MODEL_PATH = VOSK_MODEL_SMALL_FR
            elif locale == "ja":
                MODEL_PATH = VOSK_MODEL_SMALL_JA
            elif locale == "pt":
                MODEL_PATH = VOSK_MODEL_SMALL_PT
            elif locale == "zh":
                MODEL_PATH = VOSK_MODEL_SMALL_CN
            else:
                MODEL_PATH = None

            if not MODEL_PATH:
                status.update("Lorem, ipsum dolor.", state="error")
                st.stop()

            r = transcription(AUDIO_PATH, MODEL_PATH)

            # 2
            status.update(label="[3/3] Subtitling...")
            subtitling(r, SRT_PATH)

            status.update(label="Subtitling complete.", state="complete")

        st.video(
            VIDEO_PATH,
            uploaded_file.type,
            subtitles=SRT_PATH,
        )

        st.download_button(
            "Download subtitle",
            Path(SRT_PATH).read_bytes(),
            f"{uploaded_file.file_id}.srt",
            "application/octet-stream",
            use_container_width=True,
        )

    return None


if __name__ == "__main__":
    main()
