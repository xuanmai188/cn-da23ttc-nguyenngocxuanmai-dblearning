file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
content = content.replace(
    "import { XMarkIcon } from '@heroicons/react/24/outline';",
    "import { XMarkIcon } from '@heroicons/react/24/outline';\nimport { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';"
)

# 2. Add states and useEffect
state_hook = """  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });
  
  const [validations, setValidations] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  useEffect(() => {
    const p = formData.password;
    setValidations({
      length: p.length >= 8,
      uppercase: /[A-Z]/.test(p),
      lowercase: /[a-z]/.test(p),
      number: /\d/.test(p),
      special: /[!@#$%^&*(),.?":{}|<>]/ .test(p)
    });
  }, [formData.password]);

  const isPasswordValid = Object.values(validations).every(Boolean);"""

content = content.replace("  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });", state_hook)

# 3. ValidationItem component
validation_item = """  const ValidationItem = ({ label, isValid }) => (
    <div className="flex items-center space-x-2 text-sm">
      {isValid ? (
        <CheckCircleIcon className="w-5 h-5 text-green-500" />
      ) : (
        <XCircleIcon className="w-5 h-5 text-gray-300" />
      )}
      <span className={isValid ? "text-green-700" : "text-gray-500"}>{label}</span>
    </div>
  );

  const handleChange = (e) => {"""

content = content.replace("  const handleChange = (e) => {", validation_item)

# 4. Modify password JSX
old_pwd = """              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                />
              </div>"""

new_pwd = """              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mật khẩu <span className="text-red-500">*</span></label>
                <input
                  type="password"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                />
                <div className="mt-4 p-4 bg-slate-50 rounded-lg space-y-2 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wider">Yêu cầu bảo mật:</p>
                  <ValidationItem isValid={validations.length} label="Ít nhất 8 ký tự" />
                  <ValidationItem isValid={validations.uppercase} label="Có ký tự chữ IN HOA" />
                  <ValidationItem isValid={validations.lowercase} label="Có ký tự chữ thường" />
                  <ValidationItem isValid={validations.number} label="Có ký tự số" />
                  <ValidationItem isValid={validations.special} label="Có ký tự đặc biệt (!@#...)" />
                </div>
              </div>"""

content = content.replace(old_pwd, new_pwd)

# 5. Modify handleSubmit
submit_check = """    if (!isEdit && (!formData.email || !formData.password)) {
      setError('Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu (*)');
      return;
    }
    if (!isEdit && !isPasswordValid) {
      setError('Vui lòng nhập mật khẩu đáp ứng đủ các yêu cầu bảo mật.');
      return;
    }"""

content = content.replace("""    if (!isEdit && (!formData.email || !formData.password)) {
      setError('Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu (*)');
      return;
    }""", submit_check)

# 6. Disable Save button if password is not valid (only when !isEdit)
content = content.replace(
    'disabled={loading || !!fieldErrors.contact_email || !!fieldErrors.phone_number}',
    'disabled={loading || !!fieldErrors.contact_email || !!fieldErrors.phone_number || (!isEdit && !isPasswordValid)}'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserFormModal with password validation.")
