file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add fieldErrors state
content = content.replace(
    "const [error, setError] = useState('');",
    "const [error, setError] = useState('');\n  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });"
)

# 2. Add handleChange function
handleChangeStr = """  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    if (name === 'contact_email') {
      const emailRegex = /^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$/;
      if (value && !emailRegex.test(value)) {
        setFieldErrors(prev => ({ ...prev, contact_email: 'Email không hợp lệ (Ví dụ: name@gmail.com)' }));
      } else {
        setFieldErrors(prev => ({ ...prev, contact_email: '' }));
      }
    }
    
    if (name === 'phone_number') {
      const phoneRegex = /^(0|\\+84)[3|5|7|8|9][0-9]{8}$/;
      if (value && !phoneRegex.test(value)) {
        setFieldErrors(prev => ({ ...prev, phone_number: 'Phải gồm 10 số và bắt đầu bằng đầu số VN hợp lệ' }));
      } else {
        setFieldErrors(prev => ({ ...prev, phone_number: '' }));
      }
    }
  };

  const handleSubmit = async (e) => {"""

content = content.replace("  const handleSubmit = async (e) => {", handleChangeStr)

# 3. Update the submit button disabled state
content = content.replace(
    'disabled={loading}',
    'disabled={loading || !!fieldErrors.contact_email || !!fieldErrors.phone_number}'
)

# 4. Turn off native HTML5 validation
content = content.replace('<form onSubmit={handleSubmit} className="p-6 space-y-4">', '<form onSubmit={handleSubmit} className="p-6 space-y-4" noValidate>')

# 5. Update contact_email field
old_email = """          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email liên hệ (Gmail...)</label>
            <input
              type="email"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={formData.contact_email}
              onChange={e => setFormData({...formData, contact_email: e.target.value})}
              placeholder="Ví dụ: nguyenvan@gmail.com"
            />
          </div>"""

new_email = """          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email liên hệ <span className="text-red-500">*</span></label>
            <input
              type="email"
              name="contact_email"
              required
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 outline-none transition-colors ${fieldErrors.contact_email ? 'border-red-500 focus:ring-red-200' : 'border-slate-300 focus:ring-blue-500 focus:border-blue-500'}`}
              value={formData.contact_email}
              onChange={handleChange}
              placeholder="Ví dụ: nguyenvana@gmail.com"
            />
            {fieldErrors.contact_email && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.contact_email}</p>}
          </div>"""

content = content.replace(old_email, new_email)

# 6. Update phone_number field
old_phone = """          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Số điện thoại</label>
            <input
              type="tel"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={formData.phone_number}
              onChange={e => setFormData({...formData, phone_number: e.target.value})}
            />
          </div>"""

new_phone = """          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Số điện thoại <span className="text-red-500">*</span></label>
            <input
              type="tel"
              name="phone_number"
              required
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 outline-none transition-colors ${fieldErrors.phone_number ? 'border-red-500 focus:ring-red-200' : 'border-slate-300 focus:ring-blue-500 focus:border-blue-500'}`}
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="Ví dụ: 0987654321"
            />
            {fieldErrors.phone_number && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.phone_number}</p>}
          </div>"""

content = content.replace(old_phone, new_phone)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated UserFormModal.jsx successfully")
