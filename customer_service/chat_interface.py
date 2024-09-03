import streamlit as st
from st_audiorec import st_audiorec
import os
from io import BytesIO
from .response_generator import generate_response_stream
from .speech_to_text import transcribe_audio_stream
from .text_to_speech import generate_speech_stream
from .utils import format_message

def display_chat_interface():
    st.title("Assistant de Voyage IA - Évasions Élégantes")

    # Initialize chat history and conversation memory
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = {}
    if "last_audio" not in st.session_state:
        st.session_state.last_audio = None

    # Sidebar for audio recording
    with st.sidebar:
        st.header("Enregistrement Audio")
        st.write("Enregistrez votre question:")
        wav_audio_data = st_audiorec()

        if wav_audio_data is not None and wav_audio_data != st.session_state.last_audio:
            st.session_state.last_audio = wav_audio_data
            st.audio(wav_audio_data, format='audio/wav')
            st.success("Audio enregistré avec succès!")

            # Save the audio file
            if not os.path.exists('audio'):
                os.makedirs('audio')
            with open('audio/recorded_audio.wav', 'wb') as f:
                f.write(wav_audio_data)

            # Automatically process the audio
            with st.spinner("Transcription de l'audio..."):
                text = transcribe_audio_stream(wav_audio_data)
            st.session_state.messages.append(format_message("user", text))
            st.rerun()

    # Main chat interface
    chat_tab, text_input_tab = st.tabs(["Conversation", "Saisie Texte"])

    with chat_tab:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Process and display response if there's a new message
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            process_and_respond(st.session_state.messages[-1]["content"])

    with text_input_tab:
        # Text input
        text_input = st.text_input("Tapez votre question ici", key="text_input")
        if st.button("Envoyer"):
            if text_input:
                st.session_state.messages.append(format_message("user", text_input))
                st.rerun()

    # Add a button to end the conversation
    if st.button("Terminer la conversation"):
        st.write("Merci d'avoir utilisé notre assistant de voyage. À bientôt !")
        st.stop()

def process_and_respond(input_text):
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for response_chunk in generate_response_stream(st.session_state.messages, st.session_state.conversation_memory):
            full_response += response_chunk
            response_placeholder.markdown(full_response)

        response_placeholder.markdown(full_response)

    # Generate and play audio response
    try:
        st.write("Génération de la réponse vocale...")
        audio_data = generate_speech_stream(full_response)

        if audio_data:
            st.write("Audio généré avec succès. Lecture automatique...")
            st.audio(audio_data, format="audio/mp3", autoplay=True)
            st.success("Audio généré et lu avec succès !")
        else:
            st.warning("Aucune donnée audio n'a été générée.")
    except Exception as e:
        st.error(f"Erreur inattendue lors de la génération de la parole : {str(e)}")

    st.session_state.messages.append(format_message("assistant", full_response))

# Make sure to export the function
__all__ = ['display_chat_interface']