content = '''import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import LearningPath from './pages/LearningPath';
import Topics from './pages/Topics';
import TopicDetail from './pages/TopicDetail';
import LearningItem from './pages/LearningItem';
import Flashcard from './pages/Flashcard';
import Quiz from './pages/Quiz';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        
        {/* Protected Routes */}
        <Route path="/" element={<ProtectedRoute><Navigate to="/dashboard" replace /></ProtectedRoute>} />
        
        <Route path="/dashboard" element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>} />
        <Route path="/my-path" element={<ProtectedRoute><Layout><LearningPath /></Layout></ProtectedRoute>} />
        <Route path="/topics" element={<ProtectedRoute><Layout><Topics /></Layout></ProtectedRoute>} />
        <Route path="/topics/:topicId" element={<ProtectedRoute><Layout><TopicDetail /></Layout></ProtectedRoute>} />
        <Route path="/learning/:itemId" element={<ProtectedRoute><Layout><LearningItem /></Layout></ProtectedRoute>} />
        
        {/* Full screen routes (no Layout) */}
        <Route path="/flashcard/:itemId" element={<ProtectedRoute><Flashcard /></ProtectedRoute>} />
        <Route path="/quiz/:itemId" element={<ProtectedRoute><Quiz /></ProtectedRoute>} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
'''
with open('D:/DemoCN2026/dblearning/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
