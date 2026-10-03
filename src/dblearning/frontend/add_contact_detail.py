import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

contact_email_ui = """
                    <div className="flex items-center gap-3">
                      <EnvelopeIcon className="w-5 h-5 text-slate-400" />
                      <div className="flex-1">
                        <p className="text-xs text-slate-500 font-medium">Email liên hệ</p>
                        <p className="text-sm font-medium text-slate-900">{details?.contact_email || <span className="text-slate-400 italic">Chưa cập nhật</span>}</p>
                      </div>
                    </div>"""

# Insert it after the Tên đăng nhập block
target = """<p className="text-xs text-slate-500 font-medium">Tên đăng nhập</p>
                        <p className="text-sm font-medium text-slate-900">{details?.email}</p>
                      </div>
                    </div>"""

if "Email liên hệ" not in content:
    content = content.replace(target, target + contact_email_ui)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added Email liên hệ to UserDetailPanel.jsx")
