from fastapi import FastAPI
from pydantic import BaseModel

# --- Tu lógica de negocio (la misma de agente.py) ---
disponibilidad = {
    "20:00": 8,
    "21:00": 4,
    "22:00": 0,
    "23:00": 6,
}
reservas = []

def check_availability(horario, personas):
    lugares_libres = disponibilidad.get(horario)
    if lugares_libres is None:
        return {"disponible": False, "mensaje": "No atendemos en ese horario"}
    if lugares_libres < personas:
        return {"disponible": False, "mensaje": "No hay lugar en ese horario"}
    return {"disponible": True, "mensaje": "Hay lugar disponible"}

def create_reservation(nombre, horario, personas):
    resultado = check_availability(horario, personas)
    if resultado["disponible"] is False:
        return resultado
    nueva_reserva = {"nombre": nombre, "horario": horario, "personas": personas}
    reservas.append(nueva_reserva)
    disponibilidad[horario] = disponibilidad[horario] - personas
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