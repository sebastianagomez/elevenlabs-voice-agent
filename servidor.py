import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client

# Cargamos las credenciales del .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Creamos el cliente de Supabase (la conexión a la base)
supabase = create_client(supabase_url, supabase_key)

def check_availability(horario, personas):
    # Consultamos la tabla disponibilidad, filtrando por el horario pedido
    respuesta = supabase.table("disponibilidad").select("lugares_libres").eq("horario", horario).execute()

    # respuesta.data es una LISTA de filas que coinciden.
    # Si está vacía, ese horario no existe en la tabla.
    if len(respuesta.data) == 0:
        return {"disponible": False, "mensaje": "No atendemos en ese horario"}

    # Tomamos la primera (y única) fila, y de ahí el número de lugares
    lugares_libres = respuesta.data[0]["lugares_libres"]

    # De acá en adelante, la lógica es IGUAL que antes
    if lugares_libres < personas:
        return {"disponible": False, "mensaje": "No hay lugar en ese horario"}   # ← completá

    return {"disponible": True, "mensaje": "Hay lugar disponible"}

def create_reservation(nombre, horario, personas):
    # Paso 1: reutilizamos check_availability (que ahora consulta Supabase)
    resultado = check_availability(horario, personas)

    # Paso 2: si NO hay lugar, cortamos acá
    if resultado["disponible"] is False:
        return resultado

    # Paso 3: insertamos la reserva en la tabla reservas
    supabase.table("reservas").insert({
        "nombre": nombre,
        "horario": horario,
        "personas": personas
    }).execute()

    # Paso 4: descontamos los lugares ocupados de la disponibilidad.
    # Primero necesitamos saber cuántos lugares hay AHORA.
    respuesta = supabase.table("disponibilidad").select("lugares_libres").eq("horario", horario).execute()
    lugares_actuales = respuesta.data[0]["lugares_libres"]
    lugares_nuevos = lugares_actuales - personas   # ← completá: ¿qué restamos?

    # Actualizamos la fila de ese horario con el nuevo número
    supabase.table("disponibilidad").update({
        "lugares_libres": lugares_nuevos
    }).eq("horario", horario).execute()   # ← completá: ¿por cuál columna filtramos?

    # Paso 5: devolvemos confirmación
    return {"confirmada": True, "mensaje": f"Reserva confirmada para {nombre}"}

# --- El servidor web ---
app = FastAPI()

# Modelos: describen qué datos esperamos recibir en cada llamada
class DisponibilidadRequest(BaseModel):
    horario: str
    personas: int

class ReservaRequest(BaseModel):
    nombre: str
    horario: str
    personas: int

# Endpoint 1: consultar disponibilidad
@app.post("/check-availability")
def endpoint_check(datos: DisponibilidadRequest):
    return check_availability(datos.horario, datos.personas)

# Endpoint 2: crear reserva
@app.post("/create-reservation")
def endpoint_reservar(datos: ReservaRequest):
    return create_reservation(datos.nombre, datos.horario, datos.personas)   # ← completá los dos