import React, { useEffect, useState } from 'react';
import { getTasks, deleteTask } from '../services/api';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import PriorityFilter from './PriorityFilter';
import { FaPlus, FaTimes } from 'react-icons/fa';

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [editingTask, setEditingTask] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async (priority = '') => {
    try {
      setLoading(true);
      const response = await getTasks(priority);
      setTasks(response.data);
      setFilteredTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  const handlePriorityChange = (priority) => {
    fetchTasks(priority);
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    fetchTasks();
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleTaskSubmitted = () => {
    setShowForm(false);
    setEditingTask(null);
    fetchTasks();
  };

  return (
    <div className="task-list">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="mb-0">Mi Agenda</h2>
        <button 
          className={`btn ${showForm ? 'btn-outline-secondary' : 'btn-primary'}`}
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? <><FaTimes /> Cancelar</> : <><FaPlus /> Nueva Tarea</>}
        </button>
      </div>

      <PriorityFilter onPriorityChange={handlePriorityChange} />

      {showForm && (
        <div className="mb-4">
          <TaskForm 
            taskToEdit={editingTask} 
            onTaskSubmitted={handleTaskSubmitted} 
          />
        </div>
      )}

      {loading ? (
        <div className="alert alert-info text-center">Cargando tareas...</div>
      ) : filteredTasks.length === 0 ? (
        <div className="alert alert-warning text-center">No hay tareas para mostrar</div>
      ) : (
        <div className="row">
          {filteredTasks.map(task => (
            <div className="col-md-6 col-lg-4 mb-3" key={task.id}>
              <TaskItem 
                task={task} 
                onDelete={handleDelete} 
                onEdit={handleEdit} 
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskList;