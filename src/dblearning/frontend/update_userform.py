file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Add confirm_password to initial formData
content = content.replace("password: '',\n    full_name: '',", "password: '',\n    confirm_password: '',\n    full_name: '',")

# 2. Add confirmPasswordError state
content = content.replace("const [error, setError] = useState(null);", "const [error, setError] = useState(null);\n  const [confirmPasswordError, setConfirmPasswordError] = useState('');")

# 3. Handle validation in handleSubmit
old_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwordError) return;
    setSubmitting(true);
    setError(null);"""

new_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwordError) return;
    
    // Check confirm password
    if ((!user || formData.password) && formData.password !== formData.confirm_password) {
      setConfirmPasswordError('Mật khẩu nhập lại không khớp');
      return;
    }
    
    setSubmitting(true);
    setError(null);
    setConfirmPasswordError('');"""

content = content.replace(old_submit, new_submit)

# 4. Add the UI for Confirm Password
# Find the password input block and insert confirm password right after it
pwd_block_regex = r"(<div className=\"space-y-1\">\n\s*<label.*?Mật khẩu.*?</label>[\s\S]*?</div>\n\s*</div>)"

confirm_pwd_block = """\\1
        
        {(!user || formData.password) && (
          <div className="space-y-1">
            <label className="text-sm font-medium text-slate-700">
              Nhập lại mật khẩu <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="confirm_password"
                value={formData.confirm_password}
                onChange={(e) => {
                  handleChange(e);
                  if (e.target.value === formData.password) {
                    setConfirmPasswordError('');
                  } else {
                    setConfirmPasswordError('Mật khẩu nhập lại không khớp');
                  }
                }}
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors ${
                  confirmPasswordError ? 'border-red-500 focus:ring-red-500/20 focus:border-red-500' : 'border-slate-300'
                }`}
                placeholder={user ? "Nhập lại mật khẩu mới" : "••••••••"}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
              >
                {showPassword ? (
                  <EyeSlashIcon className="h-5 w-5" />
                ) : (
                  <EyeIcon className="h-5 w-5" />
                )}
              </button>
            </div>
            {confirmPasswordError && (
              <p className="text-xs text-red-500 mt-1">{confirmPasswordError}</p>
            )}
          </div>
        )}"""

content = re.sub(pwd_block_regex, confirm_pwd_block, content)

# 5. Fix password cleanup for updateData
# When updating a user, we don't send confirm_password
# Wait, updateData doesn't include confirm_password because it only includes `password` if it's not empty
# Let's check how updateData is built.
# Actually, the python script logic for `updateData` should be safe because I only added `confirm_password` to `formData`.
# The API doesn't expect `confirm_password`. If we pass it, Pydantic will ignore it if `extra=ignore` (which is default).
# But to be safe:
cleanup_replace = """    try {
      const payload = { ...formData };
      delete payload.confirm_password;"""

content = content.replace("    try {\n      if (user) {", cleanup_replace + "\n      if (user) {")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserFormModal.jsx")
