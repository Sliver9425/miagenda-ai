import React, { useEffect, useState } from 'react';
import { getTasks, deleteTask } from '../services/api';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm'; // ✅ Importar el formulario

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [editingTask, setEditingTask] = useState(null); // ✅ Tarea que se está editando
  const [showForm, setShowForm] = useState(false); // ✅ Mostrar u ocultar el formulario

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const response = await getTasks();
    setTasks(response.data);
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    fetchTasks(); // Actualizar lista
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleTaskSubmitted = () => {
    setShowForm(false);
    setEditingTask(null);
    fetchTasks(); // Recargar tareas luego de crear/editar
  };

  return (
    <div>
      <h2>Tareas</h2>

      <button onClick={() => {
        setEditingTask(null);
        setShowForm(!showForm);
      }}>
        {showForm ? 'Cancelar' : 'Crear Tarea'}
      </button>

      {showForm && (
        <TaskForm taskToEdit={editingTask} onTaskSubmitted={handleTaskSubmitted} />
      )}

      {tasks.map(task => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onDelete={handleDelete} 
          onEdit={handleEdit} // ✅ Pasar handler para editar
        />
      ))}
    </div>
  );
}

export default TaskList;

