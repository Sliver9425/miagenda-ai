def analizar_tarea(descripcion: str):
    descripcion = descripcion.lower()
    prioridad = "alta" if "urgente" in descripcion else "normal"
    tags = []
    if "estudio" in descripcion:
        tags.append("estudio")
    if "trabajo" in descripcion:
        tags.append("laboral")
    return prioridad, tags
