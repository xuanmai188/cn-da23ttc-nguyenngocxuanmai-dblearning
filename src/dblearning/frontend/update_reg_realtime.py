file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add fieldErrors state
content = content.replace("""  const [error, setError] = useState('');""", """  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({ contact_email: '', phone_number: '' });""")

# Update handleChange
old_handleChange = """  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };"""

new_handleChange = """  const handleChange = (e) => {
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
  };"""

content = content.replace(old_handleChange, new_handleChange)

# Add error texts in JSX
old_email_input = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email liên hệ <span className="text-red-500">*</span></label>
            <input
              type="email"
              name="contact_email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Ví dụ: nguyenvana@gmail.com"
              value={formData.contact_email}
              onChange={handleChange}
            />
          </div>"""

new_email_input = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email liên hệ <span className="text-red-500">*</span></label>
            <input
              type="email"
              name="contact_email"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-primary-500 outline-none transition-colors ${fieldErrors.contact_email ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-primary-500'}`}
              placeholder="Ví dụ: nguyenvana@gmail.com"
              value={formData.contact_email}
              onChange={handleChange}
            />
            {fieldErrors.contact_email && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.contact_email}</p>}
          </div>"""

content = content.replace(old_email_input, new_email_input)

old_phone_input = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại <span className="text-red-500">*</span></label>
            <input
              type="tel"
              name="phone_number"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors outline-none"
              placeholder="Ví dụ: 0987654321"
              value={formData.phone_number}
              onChange={handleChange}
            />
          </div>"""

new_phone_input = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại <span className="text-red-500">*</span></label>
            <input
              type="tel"
              name="phone_number"
              required
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-primary-500 outline-none transition-colors ${fieldErrors.phone_number ? 'border-red-500 focus:ring-red-200' : 'border-gray-300 focus:ring-primary-500'}`}
              placeholder="Ví dụ: 0987654321"
              value={formData.phone_number}
              onChange={handleChange}
            />
            {fieldErrors.phone_number && <p className="text-red-500 text-xs mt-1.5">{fieldErrors.phone_number}</p>}
          </div>"""

content = content.replace(old_phone_input, new_phone_input)

# add noValidate to form
content = content.replace('<form onSubmit={handleSubmit} className="space-y-5">', '<form onSubmit={handleSubmit} className="space-y-5" noValidate>')

# Update button disabled state
content = content.replace('disabled={isLoading || !isPasswordValid}', 'disabled={isLoading || !isPasswordValid || !!fieldErrors.contact_email || !!fieldErrors.phone_number}')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Register.jsx with real-time validation and noValidate form")
