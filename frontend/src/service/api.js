import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Cambiar en producción

export const createTask = (taskData) => axios.post(`${API_URL}/tasks/`, taskData);
export const getTasks = () => axios.get(`${API_URL}/tasks/`);
export const updateTask = (id, taskData) => axios.put(`${API_URL}/tasks/${id}`, taskData);
export const deleteTask = (id) => axios.delete(`${API_URL}/tasks/${id}`);