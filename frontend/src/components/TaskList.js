import React, { useEffect, useState } from 'react';
import { getTasks, deleteTask } from '../services/api';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import PriorityFilter from './PriorityFilter';

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
            setLoading(false);
        } catch (error) {
            console.error("Error fetching tasks:", error);
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
            <h2>Mi Agenda</h2>
            
            <div className="controls">
                <button onClick={() => setShowForm(!showForm)}>
                    {showForm ? 'Cancelar' : 'Nueva Tarea'}
                </button>
                
                <PriorityFilter onPriorityChange={handlePriorityChange} />
            </div>

            {showForm && (
                <TaskForm 
                    taskToEdit={editingTask} 
                    onTaskSubmitted={handleTaskSubmitted} 
                />
            )}

            {loading ? (
                <p>Cargando tareas...</p>
            ) : filteredTasks.length === 0 ? (
                <p>No hay tareas para mostrar</p>
            ) : (
                <div className="tasks-container">
                    {filteredTasks.map(task => (
                        <TaskItem 
                            key={task.id} 
                            task={task} 
                            onDelete={handleDelete} 
                            onEdit={handleEdit} 
                        />
                    ))}
                </div>
            )}
        </div>
    );
}

export default TaskList;