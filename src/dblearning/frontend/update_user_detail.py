import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

contact_email_ui = """                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center shrink-0">
                    <EnvelopeIcon className="w-4 h-4 text-slate-500" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs text-slate-500 font-medium">Email liên hệ</p>
                    <p className="text-sm font-medium text-slate-900 truncate">
                      {user.contact_email || <span className="text-slate-400 italic">Chưa cập nhật</span>}
                    </p>
                  </div>
                </div>"""

# Insert it after the Email block (which is now Tên đăng nhập conceptually)
content = re.sub(
    r'(<p className="text-xs text-slate-500 font-medium">Email<\/p>\s*<p className="text-sm font-medium text-slate-900 truncate">[^<]+<\/p>\s*<\/div>\s*<\/div>)',
    r'\1\n' + contact_email_ui,
    content
)

# And change the text "Email" of the first block to "Tên đăng nhập"
content = re.sub(
    r'<p className="text-xs text-slate-500 font-medium">Email<\/p>',
    r'<p className="text-xs text-slate-500 font-medium">Tên đăng nhập</p>',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserDetailPanel.jsx")
