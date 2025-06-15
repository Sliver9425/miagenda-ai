import os
import requests

def analizar_tarea(descripcion: str):
    # Primero extraemos los tags (para evitar influencia del sentimiento)
    tags = extraer_tags(descripcion)
    
    # Luego determinamos la prioridad (considerando los tags encontrados)
    prioridad = determinar_prioridad(descripcion, tags)
    
    return prioridad, tags

def determinar_prioridad(descripcion: str, tags: list) -> str:
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
        # Llamada a la API de Hugging Face con traducción previa
        result = analizar_sentimiento(descripcion)
        if result == "NEGATIVE":
            return "alta"
        else:
            return "normal"

    return "baja"

def extraer_tags(descripcion: str) -> list:
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

def traducir_espanol_ingles(texto: str) -> str:
    """Traduce el texto de español a inglés usando la API de LibreTranslate"""
    try:
        response = requests.post(
            "https://libretranslate.de/translate",
            headers={"Content-Type": "application/json"},
            json={
                "q": texto,
                "source": "es",
                "target": "en",
                "format": "text"
            }
        )
        response.raise_for_status()
        return response.json()["translatedText"]
    except Exception as e:
        print(f"Error al traducir texto: {e}")
        return texto  # Devolver texto original si falla la traducción

def analizar_sentimiento(texto: str) -> str:
    """Traduce el texto a inglés y consulta la API de Hugging Face para análisis de sentimiento"""
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    token = os.getenv("HF_TOKEN")  # Asegúrate de que la variable de entorno esté definida
    headers = {"Authorization": f"Bearer {token}"}

    texto_ingles = traducir_espanol_ingles(texto)

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": texto_ingles})
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and "label" in data[0]:
            return data[0]["label"].upper()
    except Exception as e:
        print(f"Error al analizar sentimiento: {e}")
    
    return "NEUTRAL"
