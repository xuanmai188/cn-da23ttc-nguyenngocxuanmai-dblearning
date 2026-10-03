file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Update handleAction
old_handleAction = """  const handleAction = (type, user) => {
    if (type === 'view') {
      setSelectedUser(user);
    } else if (type === 'edit') {
      setEditUser(user);
      setIsModalOpen(true);
    } else if (type === 'more') {
      alert(`Menu thao tác cho ${user.full_name}`);
    }
  };"""

new_handleAction = """  const handleAction = async (type, user) => {
    if (type === 'view') {
      setSelectedUser(user);
    } else if (type === 'edit') {
      setEditUser(user);
      setIsModalOpen(true);
    } else if (type === 'toggle_active') {
      const actionText = user.is_active ? 'khóa' : 'mở khóa';
      if (window.confirm(`Bạn có chắc chắn muốn ${actionText} tài khoản của ${user.full_name}?`)) {
        try {
          await adminApi.updateUser(user.id, { is_active: !user.is_active });
          fetchUsers(); // Refresh the list
        } catch (error) {
          console.error("Failed to toggle active status", error);
          alert('Có lỗi xảy ra khi cập nhật trạng thái.');
        }
      }
    }
  };"""

content = content.replace(old_handleAction, new_handleAction)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx")
