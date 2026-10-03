import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. formData
if "confirm_password: ''" not in content:
    content = content.replace("password: ''\n  });", "password: '',\n    confirm_password: ''\n  });")

# 2. Add confirmPasswordError state
if "confirmPasswordError" not in content:
    content = content.replace("const [error, setError] = useState('');", "const [error, setError] = useState('');\n  const [confirmPasswordError, setConfirmPasswordError] = useState('');")

# 3. Handle validation in handleSubmit
old_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isPasswordValid) return;
    setIsLoading(true);
    setError('');"""

new_submit = """const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isPasswordValid) return;
    
    // Check confirm password
    if (formData.password !== formData.confirm_password) {
      setConfirmPasswordError('Mật khẩu nhập lại không khớp');
      return;
    }
    setConfirmPasswordError('');
    
    setIsLoading(true);
    setError('');"""

if "setConfirmPasswordError('Mật khẩu nhập lại không khớp');" not in content:
    content = content.replace(old_submit, new_submit)

# 4. Add the UI for Confirm Password
old_pwd_block = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
            <input
              type="password"
              name="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Nhập mật khẩu của bạn"
              value={formData.password}
              onChange={handleChange}
            />
            
            {formData.password && !isPasswordValid && (
              <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
            )}
          </div>"""

new_pwd_block = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
            <input
              type="password"
              name="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Nhập mật khẩu của bạn"
              value={formData.password}
              onChange={handleChange}
            />
            
            {formData.password && !isPasswordValid && (
              <p className="text-red-500 text-xs mt-1.5">Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nhập lại mật khẩu <span className="text-red-500">*</span></label>
            <input
              type="password"
              name="confirm_password"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                confirmPasswordError ? 'border-red-500 focus:ring-red-200 focus:border-red-500' : 'border-gray-300 focus:ring-primary-500 focus:border-primary-500'
              }`}
              placeholder="Nhập lại mật khẩu của bạn"
              value={formData.confirm_password}
              onChange={(e) => {
                setFormData({...formData, confirm_password: e.target.value});
                if (e.target.value === formData.password) setConfirmPasswordError('');
                else setConfirmPasswordError('Mật khẩu nhập lại không khớp');
              }}
            />
            {confirmPasswordError && (
              <p className="text-red-500 text-xs mt-1.5">{confirmPasswordError}</p>
            )}
          </div>"""

if "Nhập lại mật khẩu" not in content:
    content = content.replace(old_pwd_block, new_pwd_block)

# 5. Fix payload in Register
cleanup_replace = """    try {
      const payload = { ...formData };
      delete payload.confirm_password;
      await authApi.register("""
content = content.replace("    try {\n      await authApi.register(formData);", cleanup_replace + "payload);")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Register.jsx correctly")
