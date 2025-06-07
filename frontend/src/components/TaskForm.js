function TaskForm({ taskToEdit, onTaskSubmitted }) {
  const [task, setTask] = useState(taskToEdit || { title: '', description: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = taskToEdit 
        ? await updateTask(taskToEdit.id, task) 
        : await createTask(task);
      onTaskSubmitted(response.data);
    } catch (error) {
      console.error('Error al guardar la tarea:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Título"
        value={task.title}
        onChange={(e) => setTask({ ...task, title: e.target.value })}
      />
      <textarea
        placeholder="Descripción"
        value={task.description}
        onChange={(e) => setTask({ ...task, description: e.target.value })}
      />
      <button type="submit">{taskToEdit ? 'Actualizar' : 'Crear'}</button>
    </form>
  );
}
export default TaskForm;