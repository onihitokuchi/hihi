from srt import Subtitle
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from environment import NLLB_200_DISTILLED_600M


def translation(
    results: list[Subtitle], src_lang: str, tgt_lang: str
) -> list[Subtitle]:
    r2 = results

    model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_200_DISTILLED_600M)
    tokenizer = AutoTokenizer.from_pretrained(
        NLLB_200_DISTILLED_600M,
        clean_up_tokenization_spaces=True,
    )

    translator = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        # max_length=400,
    )

    for index, res in enumerate(r2):
        output = translator(res.content)
        # TODO: Lowercase the first char, of the translated string
        r2[index].content = output[0]["translation_text"]
        print(r2[index].content)

    return r2
