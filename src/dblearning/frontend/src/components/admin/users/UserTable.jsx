import { PencilSquareIcon, EyeIcon, LockClosedIcon, LockOpenIcon } from '@heroicons/react/24/outline';

export default function UserTable({ users, loading, page, limit, total, setPage, setLimit, onAction }) {
  const totalPages = Math.ceil(total / limit);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-4 py-3 font-medium">#</th>
              <th className="px-4 py-3 font-medium">Thông tin người dùng</th>
              <th className="px-4 py-3 font-medium text-center">Vai trò</th>
              <th className="px-4 py-3 font-medium text-center">Trạng thái</th>
              <th className="px-4 py-3 font-medium">Ngày đăng ký</th>
              <th className="px-4 py-3 font-medium">Hoạt động cuối</th>
              <th className="px-4 py-3 font-medium text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 relative min-h-[200px]">
            {loading ? (
              <tr>
                <td colSpan="7" className="px-4 py-8 text-center text-slate-500">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
                  Đang tải danh sách người dùng...
                </td>
              </tr>
            ) : users.length === 0 ? (
              <tr>
                <td colSpan="7" className="px-4 py-8 text-center text-slate-500">
                  Không tìm thấy người dùng phù hợp với điều kiện lọc.
                </td>
              </tr>
            ) : (
              users.map((u, idx) => (
                <tr key={u.id} className="hover:bg-slate-50 transition-colors group">
                  <td className="px-4 py-3 text-slate-500 font-medium">
                    {(page - 1) * limit + idx + 1}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 flex-shrink-0 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-bold text-sm">
                        {(u.full_name || '').split(' ').pop().charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <div className="font-semibold text-slate-900">{u.full_name}</div>
                        <div className="text-slate-500 text-xs">{u.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`inline-flex px-2 py-1 rounded text-[11px] font-bold uppercase ${
                      u.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                    }`}>
                      {u.role === 'admin' ? 'Quản trị viên' : 'Sinh viên'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium ${
                      u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${u.is_active ? 'bg-green-500' : 'bg-red-500'}`}></span>
                      {u.is_active ? 'Hoạt động' : 'Tạm khóa'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    {new Date(u.created_at + 'Z').toLocaleDateString('vi-VN')}
                  </td>
                  <td className="px-4 py-3 text-slate-500 text-sm">
                    {u.last_activity_at || 'Chưa có hoạt động'}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button onClick={() => onAction('edit', u)} className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Chỉnh sửa">
                        <PencilSquareIcon className="w-4 h-4" />
                      </button>
                      <button onClick={() => onAction('view', u)} className="p-1.5 text-slate-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors" title="Xem chi tiết">
                        <EyeIcon className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => onAction('toggle_active', u)} 
                        className={`p-1.5 rounded-lg transition-colors ${
                          u.is_active 
                            ? 'text-slate-400 hover:text-orange-600 hover:bg-orange-50' 
                            : 'text-orange-500 hover:text-green-600 hover:bg-green-50'
                        }`} 
                        title={u.is_active ? "Khóa tài khoản" : "Mở khóa tài khoản"}
                      >
                        {u.is_active ? <LockClosedIcon className="w-4 h-4" /> : <LockOpenIcon className="w-4 h-4" />}
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="border-t border-slate-200 px-4 py-3 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-sm text-slate-500">
          Hiển thị <span className="font-medium text-slate-900">{total === 0 ? 0 : (page - 1) * limit + 1}</span> - <span className="font-medium text-slate-900">{Math.min(page * limit, total)}</span> trong <span className="font-medium text-slate-900">{total}</span> người dùng
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-500">Hiển thị</span>
            <select 
              className="border border-slate-200 rounded px-2 py-1 text-sm focus:outline-none focus:border-blue-500"
              value={limit}
              onChange={(e) => {
                setLimit(Number(e.target.value));
                setPage(1);
              }}
            >
              <option value={10}>10 / trang</option>
              <option value={20}>20 / trang</option>
              <option value={50}>50 / trang</option>
            </select>
          </div>
          
          <div className="flex items-center gap-1">
            <button 
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
              className="px-2 py-1 border border-slate-200 rounded text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50 disabled:hover:bg-transparent"
            >
              &laquo;
            </button>
            <span className="px-3 py-1 bg-blue-600 text-white rounded text-sm font-medium">
              {page}
            </span>
            <button 
              disabled={page >= totalPages}
              onClick={() => setPage(page + 1)}
              className="px-2 py-1 border border-slate-200 rounded text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50 disabled:hover:bg-transparent"
            >
              &raquo;
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
