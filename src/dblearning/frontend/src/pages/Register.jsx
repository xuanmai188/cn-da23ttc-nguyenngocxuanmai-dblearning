import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    contact_email: '',
    phone_number: ''
  });
  const [error, setError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });
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
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    if (name === 'contact_email') {
      const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
      if (value && !emailRegex.test(value)) {
        setFieldErrors(prev => ({ ...prev, contact_email: 'Email không hợp lệ (Ví dụ: name@gmail.com)' }));
      } else {
        setFieldErrors(prev => ({ ...prev, contact_email: '' }));
      }
    }
    
    if (name === 'phone_number') {
      const phoneRegex = /^(0|\+84)[3|5|7|8|9][0-9]{8}$/;
      if (value && !phoneRegex.test(value)) {
        setFieldErrors(prev => ({ ...prev, phone_number: 'Phải gồm 10 số và bắt đầu bằng đầu số VN hợp lệ' }));
      } else {
        setFieldErrors(prev => ({ ...prev, phone_number: '' }));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.full_name || !formData.email || !formData.contact_email || !formData.phone_number) {
      setError('Vui lòng điền đầy đủ các thông tin bắt buộc (*)');
      return;
    }
    if (!isPasswordValid) {
      setError('Vui lòng nhập mật khẩu đáp ứng đủ các yêu cầu bảo mật.');
      return;
    }
    
    // Validate email
    const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    if (!emailRegex.test(formData.contact_email)) {
      setError('Email liên hệ không hợp lệ. Vui lòng kiểm tra lại.');
      return;
    }

    // Validate phone (10 digits)
    const phoneRegex = /^(0|\+84)[3|5|7|8|9][0-9]{8}$/;
    if (!phoneRegex.test(formData.phone_number)) {
      setError('Số điện thoại không hợp lệ. Phải gồm 10 chữ số và bắt đầu hợp lệ ở VN.');
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

        <form onSubmit={handleSubmit} className="space-y-5" noValidate>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Họ và Tên <span className="text-red-500">*</span></label>
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Email liên hệ <span className="text-red-500">*</span></label>
            <input
              type="email"
              name="contact_email"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-primary-500 outline-none transition-colors ${fieldErrors.contact_email ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-primary-500'}`}
              placeholder="Ví dụ: nguyenvana@gmail.com"
              value={formData.contact_email}
              onChange={handleChange}
            />
            {fieldErrors.contact_email && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.contact_email}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại <span className="text-red-500">*</span></label>
            <input
              type="tel"
              name="phone_number"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-primary-500 outline-none transition-colors ${fieldErrors.phone_number ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-primary-500'}`}
              placeholder="Ví dụ: 0987654321"
              value={formData.phone_number}
              onChange={handleChange}
            />
            {fieldErrors.phone_number && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.phone_number}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tên đăng nhập <span className="text-red-500">*</span></label>
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
            <input
              type="password"
              name="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Nhập mật khẩu của bạn"
              value={formData.password}
              onChange={handleChange}
            />
            
            {formData.password && !isPasswordValid && (
              <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nhập lại mật khẩu <span className="text-red-500">*</span></label>
            <input
              type="password"
              name="confirm_password"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                confirmPasswordError ? 'border-red-500 focus:ring-red-200 focus:border-red-500' : 'border-gray-300 focus:ring-primary-500 focus:border-primary-500'
              }`}
              placeholder="Nhập lại mật khẩu của bạn"
              value={formData.confirm_password}
              onChange={(e) => {
                setFormData({...formData, confirm_password: e.target.value});
                if (e.target.value === formData.password) setConfirmPasswordError('');
                else setConfirmPasswordError('Mật khẩu nhập lại không khớp');
              }}
            />
            {confirmPasswordError && (
              <p className="text-red-500 text-xs mt-1.5">{confirmPasswordError}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading || !isPasswordValid || !!fieldErrors.contact_email || !!fieldErrors.phone_number}
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
