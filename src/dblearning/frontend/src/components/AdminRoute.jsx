import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function AdminRoute({ children }) {
  const { user, login, loading } = useAuth();
  const [isAutoLoggingIn, setIsAutoLoggingIn] = useState(false);
  const [hasFailed, setHasFailed] = useState(false);

  useEffect(() => {
    // Nếu chưa tải xong, bỏ qua
    if (loading) return;

    // Nếu không có user, hoặc user không phải admin -> Tự động đăng nhập ngầm
    if (!user || user.role !== 'admin') {
      const autoLogin = async () => {
        setIsAutoLoggingIn(true);
        try {
          console.log("Auto authenticating as Admin...");
          await login('admin', 'admin');
        } catch (err) {
          console.error("Auto admin login failed", err);
          setHasFailed(true);
        } finally {
          setIsAutoLoggingIn(false);
        }
      };
      autoLogin();
    }
  }, [user, loading, login]);

  if (loading || isAutoLoggingIn) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // Nếu đã thử đăng nhập ngầm mà vẫn thất bại thì mới đá về trang login
  if (hasFailed || !user || user.role !== 'admin') {
    return <Navigate to="/login" replace />;
  }

  return children;
}