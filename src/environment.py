from os import getenv

from dotenv import load_dotenv

load_dotenv()

VOSK_MODEL_SMALL_CN = getenv("VOSK_MODEL_SMALL_CN")
VOSK_MODEL_SMALL_EN_US = getenv("VOSK_MODEL_SMALL_EN_US")
VOSK_MODEL_SMALL_FR = getenv("VOSK_MODEL_SMALL_FR")
VOSK_MODEL_SMALL_JA = getenv("VOSK_MODEL_SMALL_JA")
VOSK_MODEL_SMALL_PT = getenv("VOSK_MODEL_SMALL_PT")
