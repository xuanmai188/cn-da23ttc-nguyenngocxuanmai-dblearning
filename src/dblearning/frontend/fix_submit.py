file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_submit = """  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {"""

new_submit = """  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Manual validation for required fields since we use noValidate
    if (!formData.full_name || !formData.contact_email || !formData.phone_number) {
      setError('Vui lòng điền đầy đủ các trường bắt buộc (*)');
      return;
    }
    if (!isEdit && (!formData.email || !formData.password)) {
      setError('Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu (*)');
      return;
    }
    if (fieldErrors.contact_email || fieldErrors.phone_number) {
      return;
    }

    setLoading(true);
    setError('');

    try {"""

content = content.replace(old_submit, new_submit)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated handleSubmit in UserFormModal.jsx")
