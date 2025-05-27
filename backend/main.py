from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import database
import ia

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str
    description: str

# Endpoints

# Crear tarea
@app.post("/tasks/")
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

# Listar tareas
@app.get("/tasks/")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# Obtener tarea por ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Actualizar tarea
@app.put("/tasks/{task_id}")
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

# Eliminar tarea
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
