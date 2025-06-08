import axios from 'axios';

const api = axios.create({
    baseURL: 'https://miagendaai-backend.onrender.com', // Cambia esta línea
    timeout: 10000, // Añade timeout de 10 segundos
    headers: {
        'Content-Type': 'application/json',
    }
});

// Configura interceptors para manejar errores globalmente
api.interceptors.response.use(
    response => response,
    error => {
        if (error.code === 'ECONNABORTED') {
            console.error('Timeout: El servidor no respondió a tiempo');
        }
        return Promise.reject(error);
    }
);

export const getTasks = (priority = '') => {
    return api.get('/tasks', {
        params: { priority }
    });
};

export const createTask = (taskData) => {
    return api.post('/tasks', taskData);
};

export const updateTask = (id, taskData) => {
    return api.put(`/tasks/${id}`, taskData);
};

export const deleteTask = (id) => {
    return api.delete(`/tasks/${id}`);
};

