import os
import time
from elevenlabs import  save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import streamlit as st

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

if not elevenlabs_api_key:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables")

# Instancier le client ElevenLabs avec la clé API
client = ElevenLabs(api_key=elevenlabs_api_key)

default_voice = Voice(
    voice_id='EXAVITQu4vr4xnSDxMaL',
    settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
)

def generate_speech_stream(text: str, voice=default_voice, output_folder='audio'):
    try:
        st.write("Generating speech...")
        audio = client.generate(
            text=text,
            voice=voice,
            model='eleven_multilingual_v2'
        )

        # Créer le dossier de sortie s'il n'existe pas
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Générer un nom de fichier unique
        output_audio_path = os.path.join(output_folder, f"response_{int(time.time())}.mp3")

        # Sauvegarder l'audio
        save(audio, output_audio_path)

        st.write(f"Audio saved to: {output_audio_path}")

        # Retourner le contenu audio pour le streaming
        with open(output_audio_path, 'rb') as audio_file:
            return audio_file.read()

    except Exception as e:
        st.error(f"Error during speech generation: {str(e)}")
        raise

# Make sure to export the function
__all__ = ['generate_speech_stream']