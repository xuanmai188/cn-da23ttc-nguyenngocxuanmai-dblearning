file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add activeTab state
content = content.replace(
    "const [limit, setLimit] = useState(10);",
    "const [limit, setLimit] = useState(10);\n  const [activeTab, setActiveTab] = useState('student');"
)

# Modify filters state to remove role
content = content.replace(
    "role: 'all',",
    ""
)

# Update fetchUsers to use activeTab instead of filters.role
content = content.replace(
    "...(filters.role !== 'all' && { role: filters.role }),",
    "role: activeTab,"
)

# Add Tab UI below Summary Cards
new_tabs = """      {/* Tabs */}
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
"""
import re
content = re.sub(r'\{\/\* Summary Cards \*\/\}\n      <UserStatsCards stats=\{stats\} \/>', 
                 "{/* Summary Cards */}\n      <UserStatsCards stats={stats} />\n\n" + new_tabs, 
                 content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx with Tabs")
