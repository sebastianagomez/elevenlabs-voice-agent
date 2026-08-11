# Agente de Voz para Reservas de Restaurante

Agente conversacional (voz y texto) que atiende llamadas de un restaurante: toma reservas, responde preguntas frecuentes y deriva reclamos a un humano. Construido sobre la plataforma de agentes de ElevenLabs, con lógica de negocio propia expuesta como webhooks y datos persistentes en una base en la nube.

> Proyecto construido para demostrar el flujo de trabajo de un Forward Deployed Engineer: entender el problema de negocio, decidir dónde aplicar IA y dónde no, integrar sistemas reales, y validar el comportamiento con evaluaciones sistemáticas.

## El problema de negocio

Un restaurante pierde reservas cuando nadie puede atender el teléfono (hora pico, poco personal, fuera de horario). Cada llamada perdida es una mesa vacía. Este agente atiende esas llamadas: resuelve lo simple de forma autónoma y deriva lo complejo a una persona.

El alcance es deliberadamente angosto —un restaurante, un caso de uso central (reservas) más un par de FAQ— en lugar de intentar automatizar todo. Decidir qué NO automatizar es parte del diseño.

## Decisiones de diseño

**Qué maneja el agente solo** (alta frecuencia + bajo riesgo):
- Tomar reservas nuevas
- Responder opciones de menú (veganas / sin TACC)

**Qué deriva a un humano** (emocional, no determinístico, relación en juego):
- Quejas y reclamos → el agente reconoce brevemente, pide el número de WhatsApp y cierra. No improvisa soluciones.

**Dónde vive cada tipo de dato:**
- Conocimiento fijo (menú, horarios) → knowledge base, se actualiza sin tocar código.
- Datos que cambian en cada llamada (disponibilidad, reservas) → base de datos (Supabase), consultada en tiempo real vía tool-calling. El agente nunca inventa disponibilidad: la consulta.

**Regla crítica:** el agente nunca confirma una mesa sin verificar disponibilidad real. El "falso sí" (confirmar una mesa que no existe) es el error más costoso, y el sistema lo hace imposible al reutilizar la verificación dentro de la creación de la reserva.

## Arquitectura

Cliente (voz/texto)
↓
Agente ElevenLabs ──consulta──> Knowledge base (menú, horarios)
↓ tool-calling
Webhooks (FastAPI)
• check-availability
• create-reservation
↓
Base de datos (Supabase)

El agente se integra sobre los sistemas del negocio en lugar de reemplazarlos: todas las reservas caen en la misma base, sin importar el canal.

## Stack

- **ElevenLabs Agents** — agente conversacional de voz/texto
- **Python + FastAPI** — webhooks que exponen la lógica de negocio
- **Supabase (PostgreSQL)** — fuente de verdad de reservas y disponibilidad
- **ngrok** — túnel para exponer el servidor local durante desarrollo

## Cómo se evalúa

El comportamiento del agente se valida con tests de simulación (evals nativos de ElevenLabs), que corren conversaciones multi-turno con un usuario simulado y evalúan la intención del resultado, no coincidencias exactas de texto. Casos cubiertos:

| Caso | Qué valida |
|---|---|
| Reserva feliz | Verifica disponibilidad, pide todos los datos, confirma y persiste |
| Sin lugar | Rechaza sin inventar disponibilidad, incluso bajo insistencia del cliente |
| Datos incompletos | Pregunta lo que falta, paso a paso, sin rechazar la llamada |
| Horario ambiguo | Pide que se especifique antes de verificar |
| Queja | Deriva a humano, va al grano, pide el WhatsApp sin dar vueltas |

Cada caso mapea a una regla de negocio del diseño. El caso "sin lugar" se probó bajo presión: el usuario simulado insistió tres veces y el agente se mantuvo firme sin ceder.

## Mejoras futuras

- Registrar las quejas en una tabla propia (webhook adicional) para que el WhatsApp quede guardado, no solo solicitado.
- Validar reservas duplicadas del mismo cliente / usar el teléfono como identificador único.
- Manejo de concurrencia en el descuento de disponibilidad (dos reservas simultáneas al mismo horario).
- Integración de voz en vivo (el sistema ya soporta voz; se probó por texto para minimizar consumo de créditos durante el desarrollo).

## Demo

_(video próximamente)_