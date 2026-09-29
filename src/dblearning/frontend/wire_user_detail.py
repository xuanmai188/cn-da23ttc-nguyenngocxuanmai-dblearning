file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Import adminApi is already there. Add LockOpenIcon to heroicons import
content = content.replace("LockClosedIcon,", "LockClosedIcon, LockOpenIcon,")

# Add handles
handles = """  const handleToggleBlock = async () => {
    if (!window.confirm(`Bạn có chắc muốn ${details?.is_active ? 'khóa' : 'mở khóa'} tài khoản này?`)) return;
    try {
      await adminApi.toggleUserStatus(user.id);
      alert('Thao tác thành công! Vui lòng tải lại trang hoặc tắt bảng chi tiết.');
      onClose(); // Close panel so user can refresh table, or better just close it.
    } catch (err) {
      alert('Lỗi: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleResetPassword = async () => {
    if (!window.confirm('Mật khẩu sẽ được đặt lại thành 123456. Bạn có chắc không?')) return;
    try {
      await adminApi.resetUserPassword(user.id);
      alert('Đã đặt lại mật khẩu thành công!');
    } catch (err) {
      alert('Lỗi: ' + (err.response?.data?.detail || err.message));
    }
  };"""

content = content.replace(
    "if (!user) return null;",
    handles + "\n\n  if (!user) return null;"
)

# Update buttons. Need to change signature to accept onEdit
content = content.replace(
    "export default function UserDetailPanel({ user, onClose }) {",
    "export default function UserDetailPanel({ user, onClose, onEdit }) {"
)

content = content.replace(
    "onClick={() => alert('Phase 4')}\n              className=\"flex items-center justify-center gap-2 px-4 py-2 bg-blue-600",
    "onClick={() => onEdit(details || user)}\n              className=\"flex items-center justify-center gap-2 px-4 py-2 bg-blue-600"
)

content = content.replace(
    """            <button 
              onClick={() => alert('Phase 4')}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
            >
              <LockClosedIcon className="w-4 h-4" />
              Khóa tài khoản
            </button>""",
    """            <button 
              onClick={handleToggleBlock}
              className={`flex items-center justify-center gap-2 px-4 py-2 text-white rounded-lg text-sm font-medium transition-colors ${details?.is_active ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
            >
              {details?.is_active ? <LockClosedIcon className="w-4 h-4" /> : <LockOpenIcon className="w-4 h-4" />}
              {details?.is_active ? 'Khóa tài khoản' : 'Mở khóa tài khoản'}
            </button>"""
)

content = content.replace(
    """          <button 
            onClick={() => alert('Phase 4')}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-300 transition-colors"
          >
            <KeyIcon className="w-4 h-4" />
            Đặt lại mật khẩu
          </button>""",
    """          <button 
            onClick={handleResetPassword}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-300 transition-colors"
          >
            <KeyIcon className="w-4 h-4" />
            Đặt lại mật khẩu
          </button>"""
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserDetailPanel.jsx with Phase 4 actions")
