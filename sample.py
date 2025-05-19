import requests
import json

def translate_text(api_key: str, target: str, text: str, model: str = "nmt") -> dict:
    """Translates text into the target language using Google Cloud Translation API."""
    url = "https://translation.googleapis.com/language/translate/v2"

    params = {
        "q": text,
        "target": target,
        "model": model,
        "key": api_key
    }

    response = requests.post(url, data=params)
    result = response.json()

    if "error" in result:
        raise Exception(f"Error: {result['error']['message']}")

    translation = result["data"]["translations"][0]

    print("Original Text:", text)
    print("Translated Text:", translation["translatedText"])

    return translation

# 사용 예시 (API 키를 여기에 입력하세요)
API_KEY = "AIzaSyA4nBnyndw2MeRgMOtyYT5F_hmy4bPcl6I"
target_language = "ja"  # 번역할 언어 (예: 한국어)
text_to_translate = "I really want to go home!! I really want it!!!"

translate_text(API_KEY, target_language, text_to_translate)