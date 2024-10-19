from transformers import WhisperProcessor, WhisperForConditionalGeneration
import sounddevice as sd

# Load the Whisper model and processor
s2t_processor = WhisperProcessor.from_pretrained("openai/whisper-small")
s2t_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")


def transcribe_audio(tensor, sr):
    forced_decoder_ids = s2t_processor.get_decoder_prompt_ids(language='russian', task='transcribe')
    s2t_input = s2t_processor(tensor, sampling_rate=sr, return_tensors="pt").input_features
    predicted_ids = s2t_model.generate(s2t_input, forced_decoder_ids=forced_decoder_ids)
    s2t_decoded = s2t_processor.batch_decode(predicted_ids, skip_special_tokens=True)

    text = ''
    for v in s2t_decoded:
        text += v

    return text


def recognize(audio_data):
    # audio_bytes = base64.b64decode(audio_data)
    # t = torch.frombuffer(audio_bytes, dtype=torch.float64)
    a = record_audio(4)
    return transcribe_audio(a['audio'], a['rate'])


def record_audio(duration=5):
    fs = 16000
    print("Запись началась...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    return {'audio': recording.squeeze(), 'rate': fs}