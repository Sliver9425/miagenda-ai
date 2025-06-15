import React, { useState } from 'react';
import { createTask, updateTask } from '../services/api';
import { Form, Button } from 'react-bootstrap';

function TaskForm({ taskToEdit, onTaskSubmitted }) {
  const [task, setTask] = useState(taskToEdit || { title: '', description: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = taskToEdit
        ? await updateTask(taskToEdit.id, task)
        : await createTask(task);
      onTaskSubmitted(response.data);
    } catch (error) {
      console.error('Error al guardar la tarea:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit} className="p-3 border rounded shadow-sm bg-white">
      <Form.Group className="mb-3">
        <Form.Label>Título</Form.Label>
        <Form.Control
          type="text"
          placeholder="Ej. Estudiar para parcial"
          value={task.title}
          onChange={(e) => setTask({ ...task, title: e.target.value })}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Descripción</Form.Label>
        <Form.Control
          as="textarea"
          rows={3}
          placeholder="Ej. Capítulos 3 al 5, enfocarse en ejercicios prácticos."
          value={task.description}
          onChange={(e) => setTask({ ...task, description: e.target.value })}
          required
        />
      </Form.Group>

      <Button variant={taskToEdit ? 'warning' : 'primary'} type="submit" disabled={loading}>
        {loading ? 'Guardando...' : taskToEdit ? 'Actualizar Tarea' : 'Crear Tarea'}
      </Button>
    </Form>
  );
}

export default TaskForm;
