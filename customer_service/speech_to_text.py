import io
from .utils import create_openai_client


def transcribe_audio_stream(audio_data: bytes):
    client = create_openai_client()

    # Create a BytesIO object from the audio data
    audio_file = io.BytesIO(audio_data)
    audio_file.name = "speech.wav"

    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text
    except Exception as e:
        print(f"Error in transcription: {e}")
        return ""