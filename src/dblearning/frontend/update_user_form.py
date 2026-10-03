import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update initial formData
content = content.replace(
    "email: user?.email || '',",
    "email: user?.email || '',\n    contact_email: user?.contact_email || '',"
)

# 2. Change Label of email to Tên đăng nhập
content = re.sub(
    r'<label className="block text-sm font-medium text-slate-700 mb-1">Email <span className="text-red-500">\*</span></label>',
    '<label className="block text-sm font-medium text-slate-700 mb-1">Tên đăng nhập <span className="text-red-500">*</span></label>',
    content
)

# 3. Add Contact Email field right after Password
contact_email_field = """            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email liên hệ (Gmail...)</label>
              <input
                type="email"
                value={formData.contact_email}
                onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ví dụ: phuminh@gmail.com"
              />
            </div>"""

content = re.sub(
    r'(<input[^>]*type="password"[^>]*/>\s*</div>)',
    r'\1\n' + contact_email_field,
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserFormModal.jsx")
