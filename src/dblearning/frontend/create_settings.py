file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Settings.jsx"
content = """import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { authApi } from '../api/authApi';
import { UserCircleIcon, KeyIcon, DevicePhoneMobileIcon, EnvelopeIcon } from '@heroicons/react/24/outline';

export default function Settings() {
  const { user } = useContext(AuthContext);
  
  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    email: '', // Email readonly for now to prevent lockout
    password: '',
    confirm_password: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (user) {
      setFormData(prev => ({
        ...prev,
        full_name: user.full_name || '',
        phone_number: user.phone_number || '',
        email: user.email || ''
      }));
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    // Validation
    if (formData.password && formData.password !== formData.confirm_password) {
      setMessage({ type: 'error', text: 'Mật khẩu xác nhận không khớp!' });
      setLoading(false);
      return;
    }

    try {
      const updateData = {
        full_name: formData.full_name,
        phone_number: formData.phone_number,
      };
      if (formData.password) {
        updateData.password = formData.password;
      }

      await authApi.updateProfile(updateData);
      
      setMessage({ type: 'success', text: 'Cập nhật thông tin thành công!' });
      
      // Clear password fields
      setFormData(prev => ({ ...prev, password: '', confirm_password: '' }));
      
      // We could ideally trigger a context reload here to update Sidebar name if needed
      // window.location.reload(); 
    } catch (err) {
      console.error(err);
      setMessage({ 
        type: 'error', 
        text: err.response?.data?.detail || 'Có lỗi xảy ra khi cập nhật.' 
      });
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto pt-6 pb-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Cài đặt Tài khoản</h1>
      
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
        
        {message && (
          <div className={`p-4 rounded-xl mb-6 font-medium ${message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Email (Readonly) */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Email đăng nhập</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <EnvelopeIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="email" 
                value={formData.email}
                disabled
                className="pl-10 w-full rounded-xl border-gray-300 bg-gray-50 text-gray-500 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <p className="mt-1 text-xs text-gray-500">Email không thể thay đổi để đảm bảo an toàn tài khoản.</p>
          </div>

          {/* Full Name */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Họ và tên</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserCircleIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="text" 
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                placeholder="Nhập họ và tên..."
              />
            </div>
          </div>

          {/* Phone Number */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Số điện thoại</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <DevicePhoneMobileIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="text" 
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                placeholder="Ví dụ: 0912345678"
              />
            </div>
          </div>

          <hr className="border-gray-100 my-8" />
          
          <h2 className="text-xl font-bold text-gray-800 mb-4">Đổi mật khẩu</h2>
          <p className="text-sm text-gray-500 mb-6">Bỏ trống nếu bạn không muốn thay đổi mật khẩu.</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Mật khẩu mới</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <KeyIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input 
                  type="password" 
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="••••••••"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Xác nhận mật khẩu</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <KeyIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input 
                  type="password" 
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>

          <div className="pt-6 mt-4 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="bg-primary-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-primary-700 transition-colors shadow-sm disabled:bg-primary-400"
            >
              {loading ? 'Đang lưu...' : 'Lưu thay đổi'}
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Settings.jsx created")
