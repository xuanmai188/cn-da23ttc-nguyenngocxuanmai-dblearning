file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
content = """import { useState, useEffect, useCallback } from 'react';
import { adminApi } from '../../api/adminApi';
import { PlusIcon } from '@heroicons/react/24/outline';
import UserStatsCards from '../../components/admin/users/UserStatsCards';
import UserFilters from '../../components/admin/users/UserFilters';
import UserTable from '../../components/admin/users/UserTable';

export default function UserManagement() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Pagination & Filters State
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [filters, setFilters] = useState({
    search: '',
    role: 'all',
    status: 'all',
    date: 'all'
  });

  const fetchStats = async () => {
    try {
      const data = await adminApi.getUserStats();
      setStats(data);
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = {
        page,
        limit,
        ...(filters.search && { search: filters.search }),
        ...(filters.role !== 'all' && { role: filters.role }),
        ...(filters.status !== 'all' && { status: filters.status }),
        ...(filters.date !== 'all' && { date: filters.date })
      };
      const data = await adminApi.getUsers(params);
      setUsers(data.users);
      setTotal(data.total);
    } catch (err) {
      setError('Lỗi khi tải danh sách người dùng. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  }, [page, limit, filters]);

  useEffect(() => {
    fetchStats();
  }, []);

  // Fetch when page or limit changes
  useEffect(() => {
    fetchUsers();
  }, [page, limit, fetchUsers]);

  const handleFilter = () => {
    setPage(1);
    fetchUsers();
  };

  const handleResetFilters = () => {
    setFilters({ search: '', role: 'all', status: 'all', date: 'all' });
    setPage(1);
    // fetchUsers will be triggered by dependency if we relied on it, but we use manual trigger for filter button
    setTimeout(() => {
      fetchUsers(); // Need to call it after state update
    }, 0);
  };

  const handleAction = (type, user) => {
    if (type === 'view') {
      alert(`Đang phát triển PHASE 3: Xem chi tiết ${user.full_name}`);
    } else if (type === 'edit') {
      alert(`Đang phát triển PHASE 4: Chỉnh sửa ${user.full_name}`);
    } else if (type === 'more') {
      alert(`Menu thao tác cho ${user.full_name}`);
    }
  };

  return (
    <div className="pb-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Quản lý người dùng</h1>
          <p className="text-slate-500 mt-1 text-sm">Quản lý tài khoản sinh viên và quản trị viên trong hệ thống</p>
        </div>
        <button 
          onClick={() => alert('Đang phát triển PHASE 4: Thêm người dùng')}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 shadow-sm transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          Thêm người dùng
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm border border-red-100 flex items-center justify-between">
          {error}
          <button onClick={fetchUsers} className="underline font-medium hover:text-red-700">Thử lại</button>
        </div>
      )}

      {/* Summary Cards */}
      <UserStatsCards stats={stats} />

      {/* Filters */}
      <UserFilters 
        filters={filters} 
        setFilters={setFilters} 
        onFilter={handleFilter} 
        onReset={handleResetFilters} 
      />

      {/* Table */}
      <UserTable 
        users={users} 
        loading={loading}
        page={page}
        limit={limit}
        total={total}
        setPage={setPage}
        setLimit={setLimit}
        onAction={handleAction}
      />
      
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
