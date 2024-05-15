from models.test_to_speech import text_to_speech
from models.frenchToFon import convert_audio_to_text, get_translation

audio_data_path = "locate.waptt.wav"
texte_french = convert_audio_to_text(audio_data_path)

source_language = 'French'
target_language = 'Fon'
translation = get_translation(source_language, target_language, texte_french)

print(translation)

text_to_speech(translation)
