import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

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

