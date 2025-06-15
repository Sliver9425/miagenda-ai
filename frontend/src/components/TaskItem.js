import React from 'react';
import { FaTrash, FaEdit } from 'react-icons/fa';

function TaskItem({ task, onDelete, onEdit }) {
  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'alta': return 'danger';
      case 'normal': return 'warning';
      case 'baja': return 'secondary';
      default: return 'light';
    }
  };

  return (
    <div className="card h-100 shadow-sm">
      <div className="card-body d-flex flex-column">
        <h5 className="card-title">{task.title}</h5>
        <p className="card-text">{task.description}</p>

        <div className="mb-2">
          <span className={`badge bg-${getPriorityBadge(task.priority)} me-2`}>
            Prioridad: {task.priority}
          </span>
          {task.tags.split(',').map((tag, i) => (
            <span key={i} className="badge bg-info me-1">{tag}</span>
          ))}
        </div>

        <div className="mt-auto d-flex gap-2">
          <button 
            className="btn btn-sm btn-outline-primary w-100"
            onClick={() => onEdit(task)}
          >
            <FaEdit className="me-1" /> Editar
          </button>
          <button 
            className="btn btn-sm btn-outline-danger w-100"
            onClick={() => onDelete(task.id)}
          >
            <FaTrash className="me-1" /> Eliminar
          </button>
        </div>
      </div>
    </div>
  );
}

export default TaskItem;