# ============================================================
#  services/llm_service.py  -->  Generación de recetas con LLM
# ============================================================
# Llama a OpenRouter (compatible con la API de OpenAI) para
# generar una receta a partir del inventario del usuario.
#
# OpenRouter permite usar modelos como LLaMA, Mistral, etc.
# La respuesta siempre es un JSON estructurado.
# ============================================================

import os
import json
import httpx
from fastapi import HTTPException

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELO_LLM = os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free")


def construir_prompt(ingredientes: list[str]) -> str:
    lista = ", ".join(ingredientes)
    return f"""Eres un chef experto. Con los siguientes ingredientes: {lista}

Genera UNA receta creativa. Responde ÚNICAMENTE con un objeto JSON válido, sin texto extra, con esta estructura exacta:

{{
  "nombre": "Nombre del plato",
  "ingredientes": ["ingrediente 1 con cantidad", "ingrediente 2 con cantidad"],
  "pasos": ["Paso 1...", "Paso 2...", "Paso 3..."],
  "tiempo_minutos": 30,
  "dificultad": "fácil"
}}

El campo "dificultad" solo puede ser: "fácil", "media" o "difícil".
No incluyas ningún texto antes ni después del JSON."""


async def generar_receta(ingredientes: list[str]) -> dict:
    """
    Llama al LLM y devuelve la receta como diccionario Python.
    Lanza HTTPException si algo falla.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY no configurada. Agrega la clave en el .env.",
        )

    if not ingredientes:
        raise HTTPException(
            status_code=400,
            detail="El inventario está vacío. Agrega ingredientes antes de generar una receta.",
        )

    prompt = construir_prompt(ingredientes)

    payload = {
        "model": MODELO_LLM,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost:8000"),
        "X-Title": "Generador de Recetas con Inventario",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            respuesta = await client.post(OPENROUTER_URL, json=payload, headers=headers)
            respuesta.raise_for_status()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="El LLM tardó demasiado. Intenta de nuevo.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error del proveedor LLM: {e.response.status_code}",
        )

    texto = respuesta.json()["choices"][0]["message"]["content"].strip()

    # Limpiamos por si el modelo manda bloques ```json ... ```
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
        texto = texto.strip()

    try:
        receta_dict = json.loads(texto)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="El LLM no devolvió un JSON válido. Intenta de nuevo.",
        )

    # Validamos que tenga los campos mínimos esperados
    campos_requeridos = {"nombre", "ingredientes", "pasos", "tiempo_minutos", "dificultad"}
    if not campos_requeridos.issubset(receta_dict.keys()):
        raise HTTPException(
            status_code=502,
            detail="La respuesta del LLM está incompleta. Intenta de nuevo.",
        )

    return receta_dict