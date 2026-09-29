import os

files = {
    'D:/DemoCN2026/dblearning/frontend/src/pages/Login.jsx': '''import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">DB Learning</h1>
          <p className="text-gray-500">Chào mừng bạn trở lại hệ thống học tập</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="nhap@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block text-sm font-medium text-gray-700">Mật khẩu</label>
              <Link to="/forgot-password" className="text-xs font-semibold text-primary-600 hover:text-primary-500">
                Quên mật khẩu?
              </Link>
            </div>
            <input
              type="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-primary-600 text-white py-2.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors focus:ring-4 focus:ring-primary-200 disabled:opacity-70 flex justify-center"
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              'Đăng nhập'
            )}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-600">
          Chưa có tài khoản?{' '}
          <Link to="/register" className="font-semibold text-primary-600 hover:text-primary-500">
            Đăng ký ngay
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
''',
    'D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx': '''import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Password validation states
  const [validations, setValidations] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  const { register } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const p = formData.password;
    setValidations({
      length: p.length >= 8,
      uppercase: /[A-Z]/.test(p),
      lowercase: /[a-z]/.test(p),
      number: /\\d/.test(p),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(p)
    });
  }, [formData.password]);

  const isPasswordValid = Object.values(validations).every(Boolean);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isPasswordValid) {
      setError('Vui lòng nhập mật khẩu đáp ứng đủ các yêu cầu bảo mật.');
      return;
    }

    setError('');
    setIsLoading(true);
    
    try {
      await register(formData);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Đăng ký thất bại. Email có thể đã tồn tại.');
    } finally {
      setIsLoading(false);
    }
  };

  const ValidationItem = ({ label, isValid }) => (
    <div className="flex items-center space-x-2 text-sm">
      {isValid ? (
        <CheckCircleIcon className="w-5 h-5 text-green-500" />
      ) : (
        <XCircleIcon className="w-5 h-5 text-gray-300" />
      )}
      <span className={isValid ? "text-green-700" : "text-gray-500"}>{label}</span>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4 py-12">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Tạo tài khoản</h1>
          <p className="text-gray-500">Bắt đầu hành trình chinh phục CSDL</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Họ và Tên</label>
            <input
              type="text"
              name="full_name"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Nguyễn Văn A"
              value={formData.full_name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="nhap@email.com"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
            <input
              type="password"
              name="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Nhập mật khẩu của bạn"
              value={formData.password}
              onChange={handleChange}
            />
            
            <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-2 border border-gray-100">
              <p className="text-xs font-semibold text-gray-600 mb-2 uppercase tracking-wider">Yêu cầu bảo mật:</p>
              <ValidationItem isValid={validations.length} label="Ít nhất 8 ký tự" />
              <ValidationItem isValid={validations.uppercase} label="Có ký tự chữ IN HOA" />
              <ValidationItem isValid={validations.lowercase} label="Có ký tự chữ thường" />
              <ValidationItem isValid={validations.number} label="Có ký tự số" />
              <ValidationItem isValid={validations.special} label="Có ký tự đặc biệt (!@#...)" />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading || !isPasswordValid}
            className="w-full bg-primary-600 text-white py-2.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors focus:ring-4 focus:ring-primary-200 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center mt-6"
          >
            {isLoading ? 'Đang xử lý...' : 'Đăng ký ngay'}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-600">
          Đã có tài khoản?{' '}
          <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-500">
            Đăng nhập
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
''',
    'D:/DemoCN2026/dblearning/frontend/src/pages/ForgotPassword.jsx': '''import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authApi } from '../api/authApi';
import { motion } from 'framer-motion';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [debugLink, setDebugLink] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setDebugLink('');
    setIsLoading(true);
    
    try {
      const response = await authApi.forgotPassword(email);
      setMessage(response.data.message);
      if (response.data.debug_reset_link) {
        setDebugLink(response.data.debug_reset_link);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra, vui lòng thử lại sau.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Quên mật khẩu?</h1>
          <p className="text-gray-500">Nhập email đã đăng ký để lấy lại mật khẩu</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        {message && (
          <div className="bg-green-50 text-green-700 p-4 rounded-lg mb-6 text-sm border border-green-200">
            <p className="font-medium">{message}</p>
            {debugLink && (
              <div className="mt-3 p-3 bg-white rounded border border-green-100 shadow-sm">
                <p className="text-xs text-gray-500 mb-1 font-semibold uppercase">Liên kết khôi phục (Chỉ dùng để Test):</p>
                <a href={debugLink} className="text-primary-600 underline break-all text-xs">
                  {debugLink}
                </a>
              </div>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="nhap@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || !email}
            className="w-full bg-primary-600 text-white py-2.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors focus:ring-4 focus:ring-primary-200 disabled:opacity-50 flex justify-center mt-6"
          >
            {isLoading ? 'Đang gửi...' : 'Gửi yêu cầu'}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-600">
          <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-500 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Quay lại đăng nhập
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
''',
    'D:/DemoCN2026/dblearning/frontend/src/pages/ResetPassword.jsx': '''import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { authApi } from '../api/authApi';
import { motion } from 'framer-motion';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  // Password validation states
  const [validations, setValidations] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  useEffect(() => {
    setValidations({
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /\\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    });
  }, [password]);

  const isPasswordValid = Object.values(validations).every(Boolean);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      setError('Liên kết không hợp lệ hoặc đã thiếu Token.');
      return;
    }
    
    if (!isPasswordValid) {
      setError('Vui lòng nhập mật khẩu đáp ứng đủ các yêu cầu bảo mật.');
      return;
    }
    
    if (password !== confirmPassword) {
      setError('Mật khẩu nhập lại không khớp.');
      return;
    }

    setError('');
    setIsLoading(true);
    
    try {
      const response = await authApi.resetPassword(token, password);
      setMessage(response.data.message);
      setIsSuccess(true);
      // Đợi 3 giây rồi chuyển hướng về login
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra, token có thể đã hết hạn.');
    } finally {
      setIsLoading(false);
    }
  };

  const ValidationItem = ({ label, isValid }) => (
    <div className="flex items-center space-x-2 text-sm">
      {isValid ? (
        <CheckCircleIcon className="w-5 h-5 text-green-500" />
      ) : (
        <XCircleIcon className="w-5 h-5 text-gray-300" />
      )}
      <span className={isValid ? "text-green-700" : "text-gray-500"}>{label}</span>
    </div>
  );

  if (!token && !isSuccess) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-xl shadow-sm text-center max-w-sm w-full">
          <XCircleIcon className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Lỗi đường dẫn</h2>
          <p className="text-gray-600 mb-6">Không tìm thấy mã khôi phục (Token) trong đường dẫn của bạn.</p>
          <Link to="/forgot-password" className="text-primary-600 font-semibold hover:underline">
            Quay lại trang Quên Mật Khẩu
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4 py-12">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8"
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Đặt lại mật khẩu</h1>
          <p className="text-gray-500">Vui lòng tạo mật khẩu mới cho tài khoản của bạn</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm">
            {error}
          </div>
        )}

        {isSuccess ? (
          <div className="text-center">
            <CheckCircleIcon className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Thành công!</h2>
            <p className="text-gray-600 mb-6">{message}</p>
            <p className="text-sm text-gray-500">Đang chuyển hướng về trang đăng nhập...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu mới</label>
              <input
                type="password"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
                placeholder="Nhập mật khẩu mới"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              
              <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-2 border border-gray-100">
                <p className="text-xs font-semibold text-gray-600 mb-2 uppercase tracking-wider">Yêu cầu bảo mật:</p>
                <ValidationItem isValid={validations.length} label="Ít nhất 8 ký tự" />
                <ValidationItem isValid={validations.uppercase} label="Có ký tự chữ IN HOA" />
                <ValidationItem isValid={validations.lowercase} label="Có ký tự chữ thường" />
                <ValidationItem isValid={validations.number} label="Có ký tự số" />
                <ValidationItem isValid={validations.special} label="Có ký tự đặc biệt (!@#...)" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Xác nhận mật khẩu</label>
              <input
                type="password"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
                placeholder="Nhập lại mật khẩu"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !isPasswordValid || password !== confirmPassword}
              className="w-full bg-primary-600 text-white py-2.5 rounded-lg font-semibold hover:bg-primary-700 transition-colors focus:ring-4 focus:ring-primary-200 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center mt-6"
            >
              {isLoading ? 'Đang xử lý...' : 'Đổi mật khẩu'}
            </button>
          </form>
        )}
      </motion.div>
    </div>
  );
}
'''
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
