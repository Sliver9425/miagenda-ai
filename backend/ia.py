import os
import requests
import time
from typing import List, Tuple

def analizar_tarea(descripcion: str) -> Tuple[str, List[str]]:
    """Analiza la descripción para determinar prioridad y tags con reintentos automáticos"""
    # Primero extraemos los tags (para evitar influencia del sentimiento)
    tags = extraer_tags(descripcion)
    
    # Luego determinamos la prioridad (considerando los tags encontrados)
    prioridad = determinar_prioridad(descripcion, tags)
    
    return prioridad, tags

def determinar_prioridad(descripcion: str, tags: List[str]) -> str:
    """Determina la prioridad basada en palabras clave y tags"""
    descripcion = descripcion.lower()
    
    palabras_alta = [
        "urgente", "importante", "necesario", "prioridad", "pronto", 
        "final", "parcial", "examen", "entrega", "plazo", "deadline"
    ]
    
    palabras_baja = [
        "opcional", "cuando pueda", "sin prisa", "tranquilo", 
        "tiempo libre", "fin de semana", "cine", "película", 
        "relaj", "diversión", "entretenimiento"
    ]
    
    for palabra in palabras_alta:
        if palabra in descripcion:
            return "alta"
            
    for palabra in palabras_baja:
        if palabra in descripcion:
            return "baja"
    
    if "estudio" in tags or "laboral" in tags:
        # Llamada a la API de Hugging Face con reintentos
        result = analizar_sentimiento_con_reintentos(descripcion)
        if result == "NEGATIVE":
            return "alta"
        else:
            return "normal"

    return "baja"

def extraer_tags(descripcion: str) -> List[str]:
    """Extrae tags basados en palabras clave"""
    descripcion = descripcion.lower()
    tags = []
    
    palabras_estudio = [
        "estudiar", "estudio", "examen", "parcial", "final", 
        "tarea", "universidad", "escuela", "aprender", "repasar",
        "apuntes", "ejercicio", "capitulo", "materia", "clase"
    ]
    
    palabras_laboral = [
        "trabajo", "oficina", "jefe", "empleo", "reunión", 
        "proyecto", "presentación", "informe", "cliente", 
        "laboral", "empresa", "equipo"
    ]
    
    palabras_entretenimiento = [
        "cine", "película", "pelicula", "juego", "diversión", 
        "fiesta", "amigos", "salir", "descanso", "ocio", 
        "relaj", "entretenimiento", "recreación", "pasatiempo"
    ]
    
    if any(palabra in descripcion for palabra in palabras_estudio):
        tags.append("estudio")
    if any(palabra in descripcion for palabra in palabras_laboral):
        tags.append("laboral")
    if any(palabra in descripcion for palabra in palabras_entretenimiento):
        tags.append("entretenimiento")
    
    return tags

def analizar_sentimiento_con_reintentos(texto: str, max_retries: int = 3) -> str:
    """Consulta a la API de Hugging Face con reintentos automáticos"""
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    token = os.getenv("HF_TOKEN")  # Asegúrate de configurar esta variable en Render
    headers = {"Authorization": f"Bearer {token}"}
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": texto},
                timeout=10  # Timeout de 10 segundos
            )
            
            # Si el modelo está cargando (503)
            if response.status_code == 503:
                estimated_time = response.json().get("estimated_time", 30)
                print(f"Modelo cargando. Intento {attempt + 1}/{max_retries}. Esperando {estimated_time} segundos...")
                time.sleep(estimated_time + 5)  # Margen adicional de 5 segundos
                continue
                
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "label" in data[0]:
                return data[0]["label"].upper()
                
        except requests.exceptions.RequestException as e:
            print(f"Error en intento {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                break
            time.sleep(5 * (attempt + 1))  # Espera progresiva: 5, 10, 15 segundos
    
    print("No se pudo obtener análisis de sentimiento después de", max_retries, "intentos")
    return "NEUTRAL"  # Valor por defecto si falla