import { useState, useEffect, useCallback } from 'react';
import { adminApi } from '../../api/adminApi';
import { PlusIcon } from '@heroicons/react/24/outline';
import UserStatsCards from '../../components/admin/users/UserStatsCards';
import UserFilters from '../../components/admin/users/UserFilters';
import UserTable from '../../components/admin/users/UserTable';
import UserDetailPanel from '../../components/admin/users/UserDetailPanel';
import UserFormModal from '../../components/admin/users/UserFormModal';

export default function UserManagement() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editUser, setEditUser] = useState(null);

  // Pagination & Filters State
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [activeTab, setActiveTab] = useState('student');
  const [filters, setFilters] = useState({
    search: '',
    
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
        role: activeTab,
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
  }, [page, limit, filters, activeTab]);

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
    setFilters({ search: '',  status: 'all', date: 'all' });
    setPage(1);
    // fetchUsers will be triggered by dependency if we relied on it, but we use manual trigger for filter button
    setTimeout(() => {
      fetchUsers(); // Need to call it after state update
    }, 0);
  };

  const handleAction = async (type, user) => {
    if (type === 'view') {
      setSelectedUser(user);
    } else if (type === 'edit') {
      setEditUser(user);
      setIsModalOpen(true);
    } else if (type === 'toggle_active') {
      const actionText = user.is_active ? 'khóa' : 'mở khóa';
      if (window.confirm(`Bạn có chắc chắn muốn ${actionText} tài khoản của ${user.full_name}?`)) {
        try {
          await adminApi.updateUser(user.id, { is_active: !user.is_active });
          fetchUsers(); // Refresh the list
        } catch (error) {
          console.error("Failed to toggle active status", error);
          alert('Có lỗi xảy ra khi cập nhật trạng thái.');
        }
      }
    }
  };

  const handleOpenAddModal = () => {
    setEditUser(null);
    setIsModalOpen(true);
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
          onClick={handleOpenAddModal}
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

      {/* Tabs */}
      <div className="flex gap-4 border-b border-slate-200 mb-6">
        <button
          onClick={() => { setActiveTab('student'); setPage(1); }}
          className={`pb-3 text-sm font-semibold transition-colors ${
            activeTab === 'student' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Danh sách Sinh viên
        </button>
        <button
          onClick={() => { setActiveTab('admin'); setPage(1); }}
          className={`pb-3 text-sm font-semibold transition-colors ${
            activeTab === 'admin' ? 'border-b-2 border-purple-600 text-purple-600' : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Danh sách Quản trị viên
        </button>
      </div>


      {/* Filters */}
      <div className="mb-6">
        <UserFilters 
          filters={filters} 
          setFilters={setFilters} 
          onFilter={handleFilter} 
          onReset={handleResetFilters} 
        />
      </div>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        <div className="flex-1 min-w-0 w-full">
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
        
        {/* Detail Panel */}
        {selectedUser && (
          <div className="w-full lg:w-[380px] shrink-0">
            <UserDetailPanel 
              user={selectedUser} 
              onClose={() => setSelectedUser(null)} 
              onEdit={(u) => { setEditUser(u); setIsModalOpen(true); }}
            />
          </div>
        )}
      </div>

      {/* Modal Thêm/Sửa */}
      <UserFormModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        user={editUser}
        onSuccess={() => {
          fetchUsers();
          fetchStats();
        }}
      />
    </div>
  );
}
