import { useState, useEffect } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';
import { adminApi } from '../../../api/adminApi';

export default function UserFormModal({ isOpen, onClose, user, onSuccess }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirm_password: '',
    contact_email: '',
    full_name: '',
    phone_number: '',
    role: 'student'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });
  
  const [validations, setValidations] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  useEffect(() => {
    const p = formData.password;
    setValidations({
      length: p.length >= 8,
      uppercase: /[A-Z]/.test(p),
      lowercase: /[a-z]/.test(p),
      number: /\d/.test(p),
      special: /[!@#$%^&*(),.?":{}|<>]/ .test(p)
    });
  }, [formData.password]);

  const isPasswordValid = Object.values(validations).every(Boolean);

  const isEdit = !!user;

  useEffect(() => {
    if (user) {
      setFormData({
        email: user.email || '',
        password: '',
        contact_email: user.contact_email || '',
        full_name: user.full_name || '',
        phone_number: user.phone_number || '',
        role: user.role || 'student'
      });
    } else {
      setFormData({
        email: '',
        password: '',
        contact_email: '',
        full_name: '',
        phone_number: '',
        role: 'student'
      });
    }
    setError('');
  }, [user, isOpen]);

  if (!isOpen) return null;

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
    
    // Manual validation for required fields since we use noValidate
    if (!formData.full_name || !formData.contact_email || !formData.phone_number) {
      setError('Vui lòng điền đầy đủ các trường bắt buộc (*)');
      return;
    }
    if (!isEdit && (!formData.email || !formData.password)) {
      setError('Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu (*)');
      return;
    }
    if (!isEdit && !isPasswordValid) {
      setError('Vui lòng nhập mật khẩu đáp ứng đủ các yêu cầu bảo mật.');
      return;
    }
    if (fieldErrors.contact_email || fieldErrors.phone_number) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      if (isEdit) {
        await adminApi.updateUser(user.id, {
          full_name: formData.full_name,
          phone_number: formData.phone_number,
          contact_email: formData.contact_email,
          role: formData.role
        });
      } else {
        await adminApi.createUser(formData);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Đã có lỗi xảy ra');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={onClose} />
      
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-900">
            {isEdit ? 'Chỉnh sửa người dùng' : 'Thêm người dùng mới'}
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4" noValidate>
          {error && (
            <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg border border-red-100">
              {error}
            </div>
          )}

          {!isEdit ? (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Tên đăng nhập <span className="text-red-500">*</span></label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
                <div className="relative">
                  <input
                    type="password"
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={formData.password}
                    onChange={e => setFormData({...formData, password: e.target.value})}
                  />
                </div>
                {formData.password && !isPasswordValid && (
                  <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Nhập lại mật khẩu <span className="text-red-500">*</span></label>
                <div className="relative">
                  <input
                    type="password"
                    required
                    className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:border-blue-500 transition-colors ${
                      confirmPasswordError ? 'border-red-500 focus:ring-red-500/20 focus:border-red-500' : 'border-slate-300 focus:ring-blue-500/20'
                    }`}
                    value={formData.confirm_password}
                    onChange={(e) => {
                      setFormData({...formData, confirm_password: e.target.value});
                      if (e.target.value === formData.password) setConfirmPasswordError('');
                      else setConfirmPasswordError('Mật khẩu nhập lại không khớp');
                    }}
                  />
                </div>
                {confirmPasswordError && (
                  <p className="text-red-500 text-xs mt-1.5">{confirmPasswordError}</p>
                )}
              </div>
            </>
          ) : (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Tên đăng nhập</label>
              <input
                type="text"
                disabled
                className="w-full px-3 py-2 border border-slate-200 bg-slate-50 text-slate-500 rounded-lg cursor-not-allowed"
                value={formData.email}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email liên hệ <span className="text-red-500">*</span></label>
            <input
              type="email"
              name="contact_email"
              required
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 outline-none transition-colors ${fieldErrors.contact_email ? 'border-red-500 focus:ring-red-200' : 'border-slate-300 focus:ring-blue-500 focus:border-blue-500'}`}
              value={formData.contact_email}
              onChange={handleChange}
              placeholder="Ví dụ: nguyenvana@gmail.com"
            />
            {fieldErrors.contact_email && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.contact_email}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Họ và tên <span className="text-red-500">*</span></label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={formData.full_name}
              onChange={e => setFormData({...formData, full_name: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Số điện thoại <span className="text-red-500">*</span></label>
            <input
              type="tel"
              name="phone_number"
              required
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 outline-none transition-colors ${fieldErrors.phone_number ? 'border-red-500 focus:ring-red-200' : 'border-slate-300 focus:ring-blue-500 focus:border-blue-500'}`}
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="Ví dụ: 0987654321"
            />
            {fieldErrors.phone_number && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.phone_number}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Vai trò</label>
            <select
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={formData.role}
              onChange={e => setFormData({...formData, role: e.target.value})}
            >
              <option value="student">Sinh viên</option>
              <option value="admin">Quản trị viên</option>
            </select>
          </div>

          <div className="flex items-center gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-slate-50 text-slate-700 font-medium rounded-lg hover:bg-slate-100 transition-colors"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={loading || !!fieldErrors.contact_email || !!fieldErrors.phone_number || (!isEdit && !isPasswordValid)}
              className="flex-1 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Đang xử lý...' : 'Lưu'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
