from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import models
import database
import ia
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://miagenda-ai.onrender.com"  # Agrega aquí tu URL real del frontend en producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    priority: str
    tags: str

    class Config:
        orm_mode = True

# Endpoints
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    priority, tags = ia.analizar_tarea(task.description)
    new_task = models.Task(
        title=task.title,
        description=task.description,
        priority=priority,
        tags=",".join(tags)
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=List[TaskResponse])
def list_tasks(
    priority: Optional[str] = Query(None, description="Filtrar por prioridad (alta, normal, baja)"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    if priority:
        if priority.lower() not in ['alta', 'normal', 'baja']:
            raise HTTPException(status_code=400, detail="Prioridad no válida")
        query = query.filter(models.Task.priority == priority.lower())
    return query.all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.description = task_data.description
    task.priority, tags = ia.analizar_tarea(task.description)
    task.tags = ",".join(tags)
    
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Endpoint raíz para evitar 404 en /
@app.get("/")
def root():
    return {"message": "MiAgendaIA backend en funcionamiento"}

# Ejecutar Uvicorn localmente si hace falta
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
