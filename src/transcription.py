import wave

from vosk import KaldiRecognizer, Model, SetLogLevel


def transcription(audio_path: str, model_path: str) -> list:
    SetLogLevel(-1)

    model = Model(model_path)

    wf = wave.open(audio_path, "rb")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []

    while True:
        data = wf.readframes(4_000)

        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = rec.Result()
            results.append(result)
            print(result)

    final_result = rec.FinalResult()
    results.append(final_result)
    print(final_result)
    return results
