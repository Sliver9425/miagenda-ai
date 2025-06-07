import React from 'react';

function TaskItem({ task, onDelete, onEdit }) {
  return (
    <div style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <p><strong>Prioridad:</strong> {task.priority}</p>
      <p><strong>Tags:</strong> {task.tags}</p>

      <button onClick={() => onEdit(task)}>Editar</button>
      <button onClick={() => onDelete(task.id)}>Eliminar</button>
    </div>
  );
}

export default TaskItem;
