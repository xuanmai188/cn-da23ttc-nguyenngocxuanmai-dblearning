import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import AdminRoute from './components/AdminRoute';
import AdminLayout from './components/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagement from './pages/admin/UserManagement';
import ContentManagement from './pages/admin/ContentManagement';
import RecommendationManagement from './pages/admin/RecommendationManagement';
import OnboardingStats from './pages/admin/OnboardingStats';
import Statistics from './pages/admin/Statistics';
import Reports from './pages/admin/Reports';
import AdminSettings from './pages/admin/AdminSettings';


import Login from './pages/Login';
import Settings from './pages/Settings';
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
        
        
        {/* Admin Routes */}
        <Route path="/admin/dashboard" element={<AdminRoute><AdminLayout><AdminDashboard /></AdminLayout></AdminRoute>} />
        <Route path="/admin/users" element={<AdminRoute><AdminLayout><UserManagement /></AdminLayout></AdminRoute>} />
        <Route path="/admin/content" element={<AdminRoute><AdminLayout><ContentManagement /></AdminLayout></AdminRoute>} />
        <Route path="/admin/recommendations" element={<AdminRoute><AdminLayout><RecommendationManagement /></AdminLayout></AdminRoute>} />
        <Route path="/admin/onboarding" element={<AdminRoute><AdminLayout><OnboardingStats /></AdminLayout></AdminRoute>} />
        <Route path="/admin/statistics" element={<AdminRoute><AdminLayout><Statistics /></AdminLayout></AdminRoute>} />
        <Route path="/admin/reports" element={<AdminRoute><AdminLayout><Reports /></AdminLayout></AdminRoute>} />
        <Route path="/admin/settings" element={<AdminRoute><AdminLayout><AdminSettings /></AdminLayout></AdminRoute>} />

        {/* Protected Routes */}
        <Route path="/" element={<ProtectedRoute><Navigate to="/dashboard" replace /></ProtectedRoute>} />
        
        <Route path="/dashboard" element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><Layout><Settings /></Layout></ProtectedRoute>} />
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
