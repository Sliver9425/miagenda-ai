
import './App.css';

// frontend/src/App.js
import TaskList from './components/TaskList';

function App() {
  return (
    <div className="container mt-4">
      <h1>Mi Agenda Universitaria</h1>
      <TaskList /> {/* Componente que lista tareas */}
    </div>
  );
}

export default App;
