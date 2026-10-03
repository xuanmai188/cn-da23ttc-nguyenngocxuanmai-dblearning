file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Change layout to grid
content = content.replace(
    '<div className="space-y-4">',
    '<div className="grid grid-cols-2 gap-y-6 gap-x-4">'
)

# Fix phone number rendering
old_phone = """                    {details?.phone_number && (
                      <div className="flex items-center gap-3">
                        <PhoneIcon className="w-5 h-5 text-slate-400" />
                        <div className="flex-1">
                          <p className="text-xs text-slate-500 font-medium">Số điện thoại</p>
                          <p className="text-sm font-medium text-slate-900">{details?.phone_number}</p>
                        </div>
                      </div>
                    )}"""

new_phone = """                    <div className="flex items-center gap-3">
                      <PhoneIcon className="w-5 h-5 text-slate-400" />
                      <div className="flex-1">
                        <p className="text-xs text-slate-500 font-medium">Số điện thoại</p>
                        <p className="text-sm font-medium text-slate-900">{details?.phone_number || <span className="text-slate-400 italic">Chưa cập nhật</span>}</p>
                      </div>
                    </div>"""

content = content.replace(old_phone, new_phone)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated grid layout successfully")
