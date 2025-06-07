import React, { useEffect, useState } from 'react';
import { getTasks, deleteTask } from '../services/api';
import TaskItem from './TaskItem';

function TaskList() {
  const [tasks, setTasks] = useState([]);

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

  return (
    <div>
      <h2>Tareas</h2>
      {tasks.map(task => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onDelete={handleDelete} 
        />
      ))}
    </div>
  );
}
