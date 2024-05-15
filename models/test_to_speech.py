import requests
import json
import base64


def text_to_speech(TEXT, VOICE_ID="21m00Tcm4TlvDq8ikWAM", YOUR_XI_API_KEY="53f8c1f40d8a497cfcaf0245b1237d72"):
    CHUNK_SIZE = 1024

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream/with-timestamps"

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": YOUR_XI_API_KEY
    }

    data = {
        "text": (
            TEXT

        ),
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        stream=True
    )

    if response.status_code != 200:
        print(f"Error encountered, status: {response.status_code}, "
              f"content: {response.text}")
        quit()

    audio_bytes = b""
    characters = []
    character_start_times_seconds = []
    character_end_times_seconds = []

    for line in response.iter_lines():
        if line:  # filter out keep-alive new line
            # convert the response which contains bytes into a JSON string from utf-8 encoding
            json_string = line.decode("utf-8")

            # parse the JSON string and load the data as a dictionary
            response_dict = json.loads(json_string)

            # the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string,
            # we need to decode it into bytes in order to save the audio as a file
            audio_bytes_chunk = base64.b64decode(response_dict["audio_base64"])
            audio_bytes += audio_bytes_chunk

            if response_dict["alignment"] is not None:
                characters.extend(response_dict["alignment"]["characters"])
                character_start_times_seconds.extend(
                    response_dict["alignment"]["character_start_times_seconds"])
                character_end_times_seconds.extend(
                    response_dict["alignment"]["character_end_times_seconds"])

    with open('FON2.mp3', 'wb') as f:
        f.write(audio_bytes)
