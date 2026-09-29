file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
content = """import { useState, useEffect } from 'react';
import { adminApi } from '../../api/adminApi';
import { motion } from 'framer-motion';
import { ShieldCheckIcon, ShieldExclamationIcon, LockClosedIcon, LockOpenIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../../context/AuthContext';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user: currentUser } = useAuth();

  const fetchUsers = async () => {
    try {
      const data = await adminApi.getUsers();
      setUsers(data.users);
    } catch (err) {
      setError('Lỗi khi tải danh sách người dùng');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleToggleStatus = async (userId) => {
    try {
      await adminApi.toggleUserStatus(userId);
      fetchUsers(); // Refresh
    } catch (err) {
      alert(err.response?.data?.detail || 'Lỗi khi đổi trạng thái');
    }
  };

  const handleToggleRole = async (userId) => {
    if (!window.confirm("Bạn có chắc muốn thay đổi quyền của người này?")) return;
    try {
      await adminApi.toggleUserRole(userId);
      fetchUsers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Lỗi khi đổi quyền');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Quản lý người dùng</h1>
          <p className="text-gray-500 mt-1">Quản lý tài khoản và phân quyền hệ thống</p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      <div className="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Học viên</th>
                <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vai trò</th>
                <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng thái</th>
                <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ngày tham gia</th>
                <th className="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Thao tác</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="h-10 w-10 flex-shrink-0 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold">
                        {u.full_name.charAt(0)}
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{u.full_name}</div>
                        <div className="text-sm text-gray-500">{u.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      u.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {u.role === 'admin' ? 'Quản trị viên' : 'Học viên'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {u.is_active ? 'Hoạt động' : 'Đã khóa'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(u.created_at).toLocaleDateString('vi-VN')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    {u.id !== currentUser?.id && (
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => handleToggleRole(u.id)}
                          className="text-gray-400 hover:text-purple-600 transition-colors"
                          title={u.role === 'admin' ? 'Hạ quyền thành Học viên' : 'Nâng cấp Quản trị viên'}
                        >
                          {u.role === 'admin' ? <ShieldExclamationIcon className="w-5 h-5" /> : <ShieldCheckIcon className="w-5 h-5" />}
                        </button>
                        <button
                          onClick={() => handleToggleStatus(u.id)}
                          className={`transition-colors ${u.is_active ? 'text-gray-400 hover:text-red-600' : 'text-red-500 hover:text-green-600'}`}
                          title={u.is_active ? 'Khóa tài khoản' : 'Mở khóa tài khoản'}
                        >
                          {u.is_active ? <LockClosedIcon className="w-5 h-5" /> : <LockOpenIcon className="w-5 h-5" />}
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("UserManagement.jsx written")
