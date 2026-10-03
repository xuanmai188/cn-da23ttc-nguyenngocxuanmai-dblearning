import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. formData
if "confirm_password:" not in content:
    content = content.replace("password: '',\n    full_name: '',", "password: '',\n    confirm_password: '',\n    full_name: '',")

# 2. Add confirmPasswordError state
if "confirmPasswordError" not in content:
    content = content.replace("const [error, setError] = useState(null);", "const [error, setError] = useState(null);\n  const [confirmPasswordError, setConfirmPasswordError] = useState('');")

# 3. Handle validation in handleSubmit
old_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Manual validation before submit"""

new_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check confirm password
    if ((!isEdit || formData.password) && formData.password !== formData.confirm_password) {
      setConfirmPasswordError('Mật khẩu nhập lại không khớp');
      return;
    }
    setConfirmPasswordError('');
    
    // Manual validation before submit"""

if "setConfirmPasswordError('Mật khẩu nhập lại không khớp');" not in content:
    content = content.replace(old_submit, new_submit)

# 4. Add the UI for Confirm Password
old_pwd_block = """              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                />
                {formData.password && !isPasswordValid && (
                  <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
                )}
              </div>"""

new_pwd_block = """              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
                <div className="relative">
                  <input
                    type="password"
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={formData.password}
                    onChange={e => setFormData({...formData, password: e.target.value})}
                  />
                </div>
                {formData.password && !isPasswordValid && (
                  <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Nhập lại mật khẩu <span className="text-red-500">*</span></label>
                <div className="relative">
                  <input
                    type="password"
                    required
                    className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:border-blue-500 transition-colors ${
                      confirmPasswordError ? 'border-red-500 focus:ring-red-500/20 focus:border-red-500' : 'border-slate-300 focus:ring-blue-500/20'
                    }`}
                    value={formData.confirm_password}
                    onChange={(e) => {
                      setFormData({...formData, confirm_password: e.target.value});
                      if (e.target.value === formData.password) setConfirmPasswordError('');
                      else setConfirmPasswordError('Mật khẩu nhập lại không khớp');
                    }}
                  />
                </div>
                {confirmPasswordError && (
                  <p className="text-red-500 text-xs mt-1.5">{confirmPasswordError}</p>
                )}
              </div>"""

if "Nhập lại mật khẩu" not in content:
    content = content.replace(old_pwd_block, new_pwd_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserFormModal.jsx correctly")
