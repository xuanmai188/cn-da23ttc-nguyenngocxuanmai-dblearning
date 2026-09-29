file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
content = """import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function UserFilters({ filters, setFilters, onFilter, onReset }) {
  const [localSearch, setLocalSearch] = useState(filters.search);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (localSearch !== filters.search) {
        setFilters(prev => ({ ...prev, search: localSearch }));
      }
    }, 500);
    return () => clearTimeout(timer);
  }, [localSearch, filters.search, setFilters]);

  // Sync when filters reset
  useEffect(() => {
    setLocalSearch(filters.search);
  }, [filters.search]);

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 mb-6 space-y-4">
      {/* Search Row */}
      <div className="relative">
        <MagnifyingGlassIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
        <input
          type="text"
          placeholder="Tìm kiếm theo tên, email, MSSV..."
          className="w-full pl-11 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors"
          value={localSearch}
          onChange={(e) => setLocalSearch(e.target.value)}
        />
      </div>
      
      {/* Filters Row */}
      <div className="flex flex-col sm:flex-row items-end justify-between gap-4">
        <div className="flex flex-wrap items-end gap-4 flex-1">
          <div className="flex-1 min-w-[150px] max-w-[200px]">
            <label className="block text-xs font-medium text-slate-500 mb-1.5">Vai trò</label>
            <select 
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              value={filters.role}
              onChange={(e) => setFilters(prev => ({ ...prev, role: e.target.value }))}
            >
              <option value="all">Tất cả</option>
              <option value="student">Sinh viên</option>
              <option value="admin">Quản trị viên</option>
            </select>
          </div>
          
          <div className="flex-1 min-w-[150px] max-w-[200px]">
            <label className="block text-xs font-medium text-slate-500 mb-1.5">Trạng thái</label>
            <select 
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            >
              <option value="all">Tất cả</option>
              <option value="active">Hoạt động</option>
              <option value="inactive">Tạm khóa</option>
            </select>
          </div>
          
          <div className="flex-1 min-w-[180px] max-w-[250px]">
            <label className="block text-xs font-medium text-slate-500 mb-1.5">Ngày đăng ký</label>
            <select 
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              value={filters.date}
              onChange={(e) => setFilters(prev => ({ ...prev, date: e.target.value }))}
            >
              <option value="all">Chọn khoảng thời gian</option>
              <option value="7days">7 ngày gần đây</option>
              <option value="30days">30 ngày gần đây</option>
              <option value="3months">3 tháng gần đây</option>
            </select>
          </div>
        </div>

        <div className="flex gap-3 w-full sm:w-auto">
          <button 
            onClick={onFilter}
            className="flex-1 sm:flex-none px-6 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm"
          >
            Lọc
          </button>
          <button 
            onClick={onReset}
            className="flex-1 sm:flex-none px-6 py-2 bg-white border border-slate-200 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors shadow-sm"
          >
            Làm lại
          </button>
        </div>
      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserFilters.jsx")
