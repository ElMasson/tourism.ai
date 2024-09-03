from elevenlabs.client import ElevenLabs
from elevenlabs import stream, set_mpv_path

client = ElevenLabs(
  api_key="sk_4acbd888ce9294df873a7b5881b4b6347018f5460092056d", # Defaults to ELEVEN_API_KEY
)

# Spécifier explicitement le chemin de mpv
mpv_path = r"D:\mpv\mpv-x86_64-20240903-git-fe4ba71\mpv.exe"
set_mpv_path(mpv_path)

audio_stream = client.generate(
  text="This is a... streaming voice!!",
  stream=True
)

stream(audio_stream)