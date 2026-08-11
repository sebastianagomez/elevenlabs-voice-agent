import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()  # Carga las variables de entorno desde el archivo .env

api_key = os.getenv("ELEVENLABS_API_KEY")

if api_key is None:
    raise ValueError("La variable de entorno ELEVENLABS_API_KEY no está definida.")

print(f"API Key: {api_key[:6]}")

client = ElevenLabs(api_key=api_key)

voces = client.voices.get_all()

print("Conexión exitosa. Cantidad de voces disponibles:", len(voces.voices))
