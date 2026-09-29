import { useState, useEffect } from 'react';
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
      number: /\d/.test(p),
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Tên đăng nhập</label>
            <input
              type="text"
              name="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Ten_dang_nhap"
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
