file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Settings.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update formData initial state
old_formdata = """  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    email: '', // Email readonly for now to prevent lockout
    password: '',
    confirm_password: ''
  });"""
new_formdata = """  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    contact_email: '',
    email: '', // Email readonly for now to prevent lockout
    password: '',
    confirm_password: ''
  });"""
content = content.replace(old_formdata, new_formdata)

# 2. Update useEffect
old_useeffect = """      setFormData(prev => ({
        ...prev,
        full_name: user.full_name || '',
        phone_number: user.phone_number || '',
        email: user.email || ''
      }));"""
new_useeffect = """      setFormData(prev => ({
        ...prev,
        full_name: user.full_name || '',
        phone_number: user.phone_number || '',
        contact_email: user.contact_email || '',
        email: user.email || ''
      }));"""
content = content.replace(old_useeffect, new_useeffect)

# 3. Update updateData
old_updatedata = """      const updateData = {
        full_name: formData.full_name,
        phone_number: formData.phone_number,
      };"""
new_updatedata = """      const updateData = {
        full_name: formData.full_name,
        phone_number: formData.phone_number,
        contact_email: formData.contact_email,
      };"""
content = content.replace(old_updatedata, new_updatedata)

# 4. Add JSX
old_jsx = """          {/* Phone Number */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Số điện thoại</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <DevicePhoneMobileIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="text" 
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                placeholder="Ví dụ: 0912345678"
              />
            </div>
          </div>"""

new_jsx = """          {/* Phone Number */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Số điện thoại</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <DevicePhoneMobileIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="tel" 
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                placeholder="Ví dụ: 0912345678"
              />
            </div>
          </div>

          {/* Contact Email */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Email liên hệ</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <EnvelopeIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="email" 
                name="contact_email"
                value={formData.contact_email}
                onChange={handleChange}
                className="pl-10 w-full rounded-xl border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                placeholder="Ví dụ: nguyenvana@gmail.com"
              />
            </div>
          </div>"""

content = content.replace(old_jsx, new_jsx)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Settings.jsx successfully")
