file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_submit = """  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isPasswordValid) {"""

new_submit = """  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.full_name || !formData.email || !formData.contact_email || !formData.phone_number) {
      setError('Vui lòng điền đầy đủ các thông tin bắt buộc (*)');
      return;
    }
    if (!isPasswordValid) {"""

if old_submit in content:
    content = content.replace(old_submit, new_submit)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated handleSubmit in Register.jsx")
else:
    print("Target not found in Register.jsx")
