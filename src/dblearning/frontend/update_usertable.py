file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserTable.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add Lock icons to import
if "LockClosedIcon" not in content:
    content = content.replace("import { PencilSquareIcon, EyeIcon, EllipsisHorizontalIcon } from '@heroicons/react/24/outline';", "import { PencilSquareIcon, EyeIcon, LockClosedIcon, LockOpenIcon } from '@heroicons/react/24/outline';")

old_button = """                      <button onClick={() => onAction('more', u)} className="p-1.5 text-slate-400 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors" title="Thêm thao tác">
                        <EllipsisHorizontalIcon className="w-4 h-4" />
                      </button>"""

new_button = """                      <button 
                        onClick={() => onAction('toggle_active', u)} 
                        className={`p-1.5 rounded-lg transition-colors ${
                          u.is_active 
                            ? 'text-slate-400 hover:text-orange-600 hover:bg-orange-50' 
                            : 'text-orange-500 hover:text-green-600 hover:bg-green-50'
                        }`} 
                        title={u.is_active ? "Khóa tài khoản" : "Mở khóa tài khoản"}
                      >
                        {u.is_active ? <LockClosedIcon className="w-4 h-4" /> : <LockOpenIcon className="w-4 h-4" />}
                      </button>"""

content = content.replace(old_button, new_button)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserTable.jsx")
