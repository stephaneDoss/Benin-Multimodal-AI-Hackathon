import io
import speech_recognition as sr
import torch
from mmtafrica import load_params, translate
from huggingface_hub import hf_hub_download

language_map = {'English': 'en', 'Swahili': 'sw', 'Fon': 'fon', 'Igbo': 'ig',
                'Kinyarwanda': 'rw', 'Xhosa': 'xh', 'Yoruba': 'yo', 'French': 'fr'}

# Load parameters and model from checkpoint
checkpoint = hf_hub_download(
    repo_id="chrisjay/mmtafrica", filename="mmt_translation.pt")
device = 'gpu' if torch.cuda.is_available() else 'cpu'
params = load_params({'checkpoint': checkpoint, 'device': device})


def get_translation(source_language, target_language, source_sentence=None):
    '''
    This takes a sentence and gets the translation.
    '''

    source_language_ = language_map[source_language]
    target_language_ = language_map[target_language]

    try:
        pred = translate(params, source_sentence,
                         source_lang=source_language_, target_lang=target_language_)
        if pred == '':
            return f"Could not find translation"
        else:
            return pred
    except Exception as error:
        return f"Issue with translation: \n {error}"


def convert_audio_to_text(audio_path):
    text = ""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        try:
            # Ajuster les paramètres de reconnaissance vocale en fonction du bruit ambiant
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)  # Enregistrez tout l'audio
            text = recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            text = "Désolé, je n'ai pas compris l'audio."
        except sr.RequestError as e:
            text = "Une erreur est survenue lors de la requête à l'API Google : {0}".format(
                e)
    return text
