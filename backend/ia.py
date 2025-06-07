from transformers import pipeline

# Cargar el modelo de clasificación de sentimientos
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def analizar_tarea(descripcion: str):
    # Analizar el sentimiento del texto
    result = classifier(descripcion)[0]
    label = result['label'].lower()  # 'positive' o 'negative'
    score = result['score']  # nivel de confianza (0-1)
    
    # Determinar prioridad basada en sentimiento y palabras clave
    prioridad = determinar_prioridad(descripcion, label, score)
    
    # Extraer tags basados en palabras clave
    tags = extraer_tags(descripcion)
    
    return prioridad, tags

def determinar_prioridad(descripcion: str, sentimiento: str, confianza: float) -> str:
    """Determina la prioridad basada en sentimiento, confianza y palabras clave"""
    descripcion = descripcion.lower()
    
    # Palabras clave que indican alta prioridad
    palabras_alta = ["urgente", "importante", "necesario", "prioridad", "pronto"]
    # Palabras clave que indican baja prioridad
    palabras_baja = ["opcional", "cuando pueda", "sin prisa", "tranquilo", "cuando tengas tiempo"]
    
    # Si encuentra palabras clave explícitas
    for palabra in palabras_alta:
        if palabra in descripcion:
            return "alta"
            
    for palabra in palabras_baja:
        if palabra in descripcion:
            return "baja"
    
    # Si no hay palabras clave, usar el sentimiento del texto
    if sentimiento == 'positive':
        return "baja" if confianza > 0.9 else "normal"
    else:
        return "alta" if confianza > 0.7 else "normal"

def extraer_tags(descripcion: str) -> list:
    """Extrae tags basados en palabras clave en la descripción"""
    descripcion = descripcion.lower()
    tags = []
    
    # Palabras clave para cada categoría
    palabras_estudio = ["estudio", "examen", "tarea", "universidad", "escuela", "aprender"]
    palabras_laboral = ["trabajo", "oficina", "jefe", "empleo", "reunión", "proyecto"]
    palabras_entretenimiento = ["cine", "película", "juego", "diversión", "fiesta", "amigos"]
    
    # Verificar cada categoría
    if any(palabra in descripcion for palabra in palabras_estudio):
        tags.append("estudio")
    if any(palabra in descripcion for palabra in palabras_laboral):
        tags.append("laboral")
    if any(palabra in descripcion for palabra in palabras_entretenimiento):
        tags.append("entretenimiento")
    
    return tags