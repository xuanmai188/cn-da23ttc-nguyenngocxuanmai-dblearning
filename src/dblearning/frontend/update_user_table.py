import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserTable.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Change the display from:
# <p className="text-sm font-bold text-slate-800">{user.full_name}</p>
# <p className="text-xs text-slate-500 mt-0.5">{user.email}</p>
# to:
# <p className="text-sm font-bold text-slate-800">{user.full_name}</p>
# <p className="text-xs text-slate-500 mt-0.5">{user.email} {user.contact_email ? `• ${user.contact_email}` : ''}</p>

content = re.sub(
    r'<p className="text-xs text-slate-500 mt-0\.5">\{user\.email\}<\/p>',
    r'<p className="text-xs text-slate-500 mt-0.5">{user.email} {user.contact_email ? `• ${user.contact_email}` : \'\'}</p>',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserTable.jsx")
