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
            sl = SRC_LANG[src_lang]
            tl = TGT_LANG[tgt_lang]
            same_lang = sl == tl
            number_of_jobs = 5
            if same_lang:
                number_of_jobs = 4

            # 0
            status.update(label=f"[1/{number_of_jobs}] Audio extraction...")

            AUDIO_PATH = extraction(
                VIDEO_PATH, str(PATH.joinpath(f"{uploaded_file.file_id}.wav"))
            )

            # 1
            status.update(label=f"[2/{number_of_jobs}] Transcription...")

            if sl == "eng_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_EN_US
            elif sl == "fra_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_FR
            elif sl == "jpn_Jpan":
                MODEL_PATH = VOSK_MODEL_SMALL_JA
            elif sl == "por_Latn":
                MODEL_PATH = VOSK_MODEL_SMALL_PT
            elif sl == "zho_Hans" or sl == "zho_Hant":
                MODEL_PATH = VOSK_MODEL_SMALL_CN
            else:
                MODEL_PATH = None

            if not MODEL_PATH:
                status.update(label="Lorem, ipsum dolor.", state="error")
                st.stop()

            r = transcription(AUDIO_PATH, MODEL_PATH)

            # 2
            status.update(label=f"[3/{number_of_jobs}] Subtitling...")
            s1 = subtitling0(r, SRT_PATH)

            print(
                "================================================================================="
            )
            # 3
            if same_lang:
                status.update(
                    label=f"[{number_of_jobs}/{number_of_jobs}] Saving subtitle..."
                )
                subtitling(s1, SRT_PATH)
            else:
                status.update(label=f"[4/{number_of_jobs}] Translation...")
                s2 = translation(s1, sl, tl)

                status.update(
                    label=f"[{number_of_jobs}/{number_of_jobs}] Saving subtitle..."
                )
                subtitling(s2, SRT_PATH)

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
