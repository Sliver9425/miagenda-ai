from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def analizar_tarea(descripcion: str):
    # Primero extraemos los tags (para evitar influencia del sentimiento)
    tags = extraer_tags(descripcion)
    
    # Luego determinamos la prioridad (considerando los tags encontrados)
    prioridad = determinar_prioridad(descripcion, tags)
    
    return prioridad, tags

def determinar_prioridad(descripcion: str, tags: list) -> str:
    """Determina la prioridad basada en palabras clave y tags"""
    descripcion = descripcion.lower()
    
    # Palabras clave que siempre indican alta prioridad
    palabras_alta = [
        "urgente", "importante", "necesario", "prioridad", "pronto", 
        "final", "parcial", "examen", "entrega", "plazo", "deadline"
    ]
    
    # Palabras clave que indican baja prioridad
    palabras_baja = [
        "opcional", "cuando pueda", "sin prisa", "tranquilo", 
        "tiempo libre", "fin de semana", "cine", "película", 
        "relaj", "diversión", "entretenimiento"
    ]
    
    # 1. Verificar palabras clave explícitas primero
    for palabra in palabras_alta:
        if palabra in descripcion:
            return "alta"
            
    for palabra in palabras_baja:
        if palabra in descripcion:
            return "baja"
    
    # 2. Si no hay palabras clave, analizar por tags
    if "estudio" in tags or "laboral" in tags:
        # Solo usar el modelo de sentimientos para estos casos
        result = classifier(descripcion)[0]
        label = result['label'].lower()
        
        if label == 'negative':
            return "alta"
        else:
            return "normal"
    
    # 3. Para entretenimiento y casos sin tags específicos
    return "baja"

def extraer_tags(descripcion: str) -> list:
    """Extrae tags basados en palabras clave en la descripción"""
    descripcion = descripcion.lower()
    tags = []
    
    # Palabras clave ampliadas para cada categoría
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
    
    # Verificar cada categoría
    if any(palabra in descripcion for palabra in palabras_estudio):
        tags.append("estudio")
    if any(palabra in descripcion for palabra in palabras_laboral):
        tags.append("laboral")
    if any(palabra in descripcion for palabra in palabras_entretenimiento):
        tags.append("entretenimiento")
    
    return tags