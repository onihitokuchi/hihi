from pathlib import Path

import streamlit as st

from environment import (
    SRC_LANG,
    TGT_LANG,
    VOSK_MODEL_SMALL_CN,
    VOSK_MODEL_SMALL_EN_US,
    VOSK_MODEL_SMALL_FR,
    VOSK_MODEL_SMALL_JA,
    VOSK_MODEL_SMALL_PT,
)
from extraction import extraction
from subtitling import subtitling, subtitling0
from transcription import transcription
from translation import translation


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

    column_1, column_2 = st.columns(2)
    with column_1:
        src_lang = st.selectbox(
            "Translate from", options=list(SRC_LANG.keys()), index=5
        )
    with column_2:
        tgt_lang = st.selectbox("Translate to", options=list(TGT_LANG.keys()), index=3)

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
            status.update(label="[1/4] Audio extraction...")

            AUDIO_PATH = extraction(
                VIDEO_PATH, str(PATH.joinpath(f"{uploaded_file.file_id}.wav"))
            )

            # 1
            status.update(label="[2/4] Transcription...")
            s = SRC_LANG[src_lang]

            if s == "eng_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_EN_US
            elif s == "fra_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_FR
            elif s == "jpn_Jpan":
                MODEL_PATH = VOSK_MODEL_SMALL_JA
            elif s == "por_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_PT
            elif s == "zho_Hans" or s == "zho_Hant":
                MODEL_PATH = VOSK_MODEL_SMALL_CN
            else:
                MODEL_PATH = None

            if not MODEL_PATH:
                status.update(label="Lorem, ipsum dolor.", state="error")
                st.stop()

            r = transcription(AUDIO_PATH, MODEL_PATH)

            # 2
            status.update(label="[3/4] Subtitling...")
            s = subtitling0(r, SRT_PATH)

            print(
                "================================================================================="
            )
            # 3
            status.update(label="[4/4] Translation...")
            r2 = translation(s, SRC_LANG[src_lang], TGT_LANG[tgt_lang])

            status.update(label="[5/5] Saving subtitle...")
            subtitling(r2, SRT_PATH)

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
