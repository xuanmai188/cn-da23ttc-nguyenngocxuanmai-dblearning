file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

target_block = """                <div className="mt-4 p-4 bg-slate-50 rounded-lg space-y-2 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wider">Yêu cầu bảo mật:</p>
                  <ValidationItem isValid={validations.length} label="Ít nhất 8 ký tự" />
                  <ValidationItem isValid={validations.uppercase} label="Có ký tự chữ IN HOA" />
                  <ValidationItem isValid={validations.lowercase} label="Có ký tự chữ thường" />
                  <ValidationItem isValid={validations.number} label="Có ký tự số" />
                  <ValidationItem isValid={validations.special} label="Có ký tự đặc biệt (!@#...)" />
                </div>"""

# Remove the block but keep a small hint text
replacement = """                {formData.password && !isPasswordValid && (
                  <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
                )}"""

if target_block in content:
    content = content.replace(target_block, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Removed visual checklist from UserFormModal.jsx")
else:
    print("Could not find the target block.")
