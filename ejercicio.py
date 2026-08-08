import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

respuesta = client.voices.get_all()
voces = respuesta.voices

mapa = {}

for voz in voces:    
    print(f"Nombre: {voz.name}")
    mapa[voz.name] = voz.voice_id

for nombre, voice_id in mapa.items():
    print(f"{nombre} → {voice_id}")
    
print(mapa)
print("Conexión exitosa. Cantidad de voces disponibles:", len(respuesta.voices))
