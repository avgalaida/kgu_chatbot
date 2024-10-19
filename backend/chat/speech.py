import torch
import base64

import soundfile as sf
import sounddevice as sd

language = 'ru'
model_id = 'v4_ru'
sample_rate = 48_000
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


def generate_speech(text, speaker):
    audio = model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=sample_rate)

    sf.write('temp.wav', audio.numpy(), sample_rate)
    data, samplerate = sf.read('temp.wav')
    sd.play(data, samplerate)
    sd.wait()

    audio_bytes = audio.numpy().tobytes()
    b64 = base64.b64encode(audio_bytes).decode('utf-8')

    return str(b64)
