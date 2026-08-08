# Simulamos la disponibilidad del restaurante.
# Clave = horario, Valor = cantidad de lugares libres en ese horario.
disponibilidad = {
    "20:00": 8,
    "21:00": 4,
    "22:00": 0,   # este horario está lleno
    "23:00": 6,
}
# Acá se van acumulando las reservas confirmadas (simula la tabla de Supabase)
reservas = []

def check_availability(horario, personas):
    lugares_libres = disponibilidad.get(horario)

    if lugares_libres is None:
        return {"disponible": False, "mensaje": "No atendemos en ese horario"}

    if lugares_libres < personas:
        return {"disponible": False, "mensaje": "No hay lugar en ese horario"}

    return {"disponible": True, "mensaje": "Hay lugar disponible"}

def create_reservation(nombre, horario, personas):
    # Paso 1: reutilizamos check_availability para no guardar a ciegas
    resultado = check_availability(horario, personas)

    # Paso 2: si NO hay lugar, cortamos acá y devolvemos el porqué
    if resultado["disponible"] is False:      # ← completá: ¿False o True? (queremos cortar cuando NO hay)
        return resultado

    # Paso 3: hay lugar. Armamos la reserva como un diccionario
    nueva_reserva = {
        "nombre": nombre,
        "horario": horario,
        "personas": personas
    }

    # La guardamos en la lista
    reservas.append(nueva_reserva)

    # Descontamos los lugares ocupados de la disponibilidad
    disponibilidad[horario] = disponibilidad[horario] - personas   # ← completá: ¿qué restamos?

    # Devolvemos confirmación estructurada
    return {"confirmada": True, "mensaje": f"Reserva confirmada para {nombre}"}


# Probamos: incluí un caso feliz y uno infeliz
print(create_reservation("Sebi", "20:00", 4))    # esperamos: confirmada
print(create_reservation("Ana", "22:00", 2))     # esperamos: rechazada (22:00 está lleno)
print(reservas)                                   # esperamos ver la reserva de Sebi guardada
print(check_availability("20:00", 6))