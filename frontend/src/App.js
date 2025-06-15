import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, Navigate } from 'react-router-dom';
import TaskList from './components/TaskList';
import SignIn from './pages/SignIn.jsx';
import { FaClipboardList } from 'react-icons/fa';

function App() {
  return (
    <>
      {/* Barra de navegación */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div className="container">
          <span className="navbar-brand d-flex align-items-center">
            <FaClipboardList className="me-2" />
            Mi Agenda Universitaria
          </span>
        </div>
      </nav>

      {/* Contenido principal con rutas */}
      <main className="container py-4">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<SignIn />} />
          <Route path="/tasks" element={<TaskList />} />
        </Routes>
      </main>
    </>
  );
}

export default App;



