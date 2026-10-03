file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Add confirm_password to initial formData
content = content.replace("password: ''\n  });", "password: '',\n    confirm_password: ''\n  });")

# 2. Add confirmPasswordError state
content = content.replace("const [passwordError, setPasswordError] = useState('');", "const [passwordError, setPasswordError] = useState('');\n  const [confirmPasswordError, setConfirmPasswordError] = useState('');")

# 3. Handle validation in handleSubmit
old_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwordError) return;
    setLoading(true);
    setError(null);"""

new_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwordError) return;
    
    // Check confirm password
    if (formData.password !== formData.confirm_password) {
      setConfirmPasswordError('Mật khẩu nhập lại không khớp');
      return;
    }
    
    setLoading(true);
    setError(null);
    setConfirmPasswordError('');"""

content = content.replace(old_submit, new_submit)

# 4. Add the UI for Confirm Password
pwd_block_regex = r"(<div>\n\s*<label.*?Mật khẩu.*?</label>[\s\S]*?</div>\n\s*</div>)"

confirm_pwd_block = """\\1
            
            <div>
              <label htmlFor="confirm_password" className="block text-sm font-semibold text-gray-700 mb-2">
                Nhập lại mật khẩu <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirm_password"
                  name="confirm_password"
                  type={showPassword ? "text" : "password"}
                  required
                  value={formData.confirm_password}
                  onChange={(e) => {
                    handleChange(e);
                    if (e.target.value === formData.password) {
                      setConfirmPasswordError('');
                    } else {
                      setConfirmPasswordError('Mật khẩu nhập lại không khớp');
                    }
                  }}
                  className={`pl-10 pr-10 w-full rounded-xl shadow-sm focus:border-primary-500 focus:ring-primary-500 ${
                    confirmPasswordError ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5" aria-hidden="true" />
                  ) : (
                    <EyeIcon className="h-5 w-5" aria-hidden="true" />
                  )}
                </button>
              </div>
              {confirmPasswordError && (
                <p className="mt-1 text-xs text-red-500">{confirmPasswordError}</p>
              )}
            </div>"""

content = re.sub(pwd_block_regex, confirm_pwd_block, content)

# 5. Fix updateData / Payload
cleanup_replace = """    try {
      const payload = { ...formData };
      delete payload.confirm_password;
      await authApi.register("""
content = content.replace("    try {\n      await authApi.register(formData);", cleanup_replace + "payload);")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Register.jsx")
