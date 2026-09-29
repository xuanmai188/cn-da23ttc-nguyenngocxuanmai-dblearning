file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update subtitle
content = content.replace("Quản lý tài khoản và phân quyền hệ thống", "Danh sách học viên trên hệ thống")

# Filter out admin
content = content.replace("{users.map((u) => (", "{users.filter(u => u.role !== 'admin').map((u) => (")

# Remove Role header
content = content.replace("<th className=\"px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider\">Vai trò</th>", "")

# Remove Role data cell
role_td = """                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      u.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {u.role === 'admin' ? 'Quản trị viên' : 'Học viên'}
                    </span>
                  </td>"""
content = content.replace(role_td, "")

# Remove handleToggleRole button
toggle_role_btn = """                        <button
                          onClick={() => handleToggleRole(u.id)}
                          className="text-gray-400 hover:text-purple-600 transition-colors"
                          title={u.role === 'admin' ? 'Hạ quyền thành Học viên' : 'Nâng cấp Quản trị viên'}
                        >
                          {u.role === 'admin' ? <ShieldExclamationIcon className="w-5 h-5" /> : <ShieldCheckIcon className="w-5 h-5" />}
                        </button>"""
content = content.replace(toggle_role_btn, "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx")
