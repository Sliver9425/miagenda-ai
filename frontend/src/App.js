import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useClerk, SignedIn } from '@clerk/clerk-react';
import TaskList from './components/TaskList.js';
import SignIn from './pages/SignIn.jsx';
import { FaClipboardList } from 'react-icons/fa';
import { Button } from 'react-bootstrap';
import ProtectedRoute from './components/ProtectedRoute'; // 👈 nuevo

function App() {
  const { signOut } = useClerk();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await signOut();
    navigate('/login');
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div className="container d-flex justify-content-between align-items-center">
          <span className="navbar-brand d-flex align-items-center">
            <FaClipboardList className="me-2" />
            Mi Agenda Universitaria
          </span>

          <SignedIn>
            <Button variant="outline-light" onClick={handleLogout}>
              Logout
            </Button>
          </SignedIn>
        </div>
      </nav>

      <main className="container py-4">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<SignIn />} />
          <Route
            path="/tasks"
            element={
              <ProtectedRoute>
                <TaskList />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </>
  );
}

export default App;




