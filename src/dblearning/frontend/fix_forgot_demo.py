file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/ForgotPassword.jsx"

new_content = """import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authApi } from '../api/authApi';
import { motion } from 'framer-motion';
import { EnvelopeIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [debugLink, setDebugLink] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setDebugLink('');
    setIsLoading(true);
    
    try {
      const response = await authApi.forgotPassword(email);
      setMessage(response.message);
      if (response.debug_reset_link) {
        setDebugLink(response.debug_reset_link);
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
        className="max-w-md w-full"
      >
        {/* Main card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="mx-auto w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
              <EnvelopeIcon className="w-8 h-8 text-primary-600" />
            </div>
            <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Quên mật khẩu?</h1>
            <p className="text-gray-500">Nhập email đã đăng ký để lấy lại mật khẩu</p>
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm">
              {error}
            </div>
          )}

          {message ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              {/* Success state */}
              <div className="text-center mb-6">
                <CheckCircleIcon className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <p className="text-green-700 font-semibold text-lg">Email đã được gửi!</p>
                <p className="text-gray-500 text-sm mt-1">Kiểm tra hộp thư của bạn và bấm vào link để đặt lại mật khẩu.</p>
              </div>

              {/* Simulated Email Preview (Demo only) */}
              {debugLink && (
                <div className="border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                  {/* Email header */}
                  <div className="bg-gray-50 border-b border-gray-200 px-4 py-3">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-gray-500 w-10">Từ:</span>
                      <span className="text-xs text-gray-700">noreply@dblearning.edu.vn</span>
                    </div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-gray-500 w-10">Đến:</span>
                      <span className="text-xs text-gray-700">{email}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-gray-500 w-10">Tiêu đề:</span>
                      <span className="text-xs text-gray-700 font-medium">[DB Learning] Đặt lại mật khẩu của bạn</span>
                    </div>
                  </div>
                  
                  {/* Email body */}
                  <div className="bg-white p-4">
                    <p className="text-sm text-gray-700 mb-3">Xin chào,</p>
                    <p className="text-sm text-gray-700 mb-4">
                      Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn. 
                      Bấm vào nút bên dưới để tiếp tục:
                    </p>
                    <a
                      href={debugLink}
                      className="block w-full text-center bg-primary-600 text-white py-2.5 px-4 rounded-lg font-semibold hover:bg-primary-700 transition-colors text-sm"
                    >
                      Đặt lại mật khẩu
                    </a>
                    <p className="text-xs text-gray-400 mt-4 text-center">
                      Link có hiệu lực trong 15 phút. Nếu không phải bạn, hãy bỏ qua email này.
                    </p>
                  </div>

                  {/* Demo badge */}
                  <div className="bg-amber-50 border-t border-amber-200 px-4 py-2 flex items-center gap-2">
                    <span className="text-xs text-amber-700">
                      🔧 <strong>Chế độ Demo:</strong> Email mô phỏng hiển thị trực tiếp thay vì gửi vào hộp thư
                    </span>
                  </div>
                </div>
              )}

              <button
                onClick={() => { setMessage(''); setDebugLink(''); setEmail(''); }}
                className="w-full mt-4 text-center text-sm text-primary-600 hover:underline"
              >
                Gửi lại email khác
              </button>
            </motion.div>
          ) : (
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
          )}
        </div>

        <p className="mt-6 text-center text-sm text-gray-600">
          <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-500 flex items-center justify-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Quay lại đăng nhập
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("ForgotPassword.jsx updated with simulated email UI")
