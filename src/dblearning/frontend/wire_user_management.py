file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import UserDetailPanel from '../../components/admin/users/UserDetailPanel';",
    "import UserDetailPanel from '../../components/admin/users/UserDetailPanel';\nimport UserFormModal from '../../components/admin/users/UserFormModal';"
)

content = content.replace(
    "const [selectedUser, setSelectedUser] = useState(null);",
    "const [selectedUser, setSelectedUser] = useState(null);\n  const [isModalOpen, setIsModalOpen] = useState(false);\n  const [editUser, setEditUser] = useState(null);"
)

# Fix handleAction in UserManagement.jsx
new_handle_action = """const handleAction = (type, user) => {
    if (type === 'view') {
      setSelectedUser(user);
    } else if (type === 'edit') {
      setEditUser(user);
      setIsModalOpen(true);
    } else if (type === 'more') {
      alert(`Menu thao tác cho ${user.full_name}`);
    }
  };

  const handleOpenAddModal = () => {
    setEditUser(null);
    setIsModalOpen(true);
  };"""

import re
content = re.sub(r'const handleAction = \(type, user\) => \{.*?\};', new_handle_action, content, flags=re.DOTALL)

content = content.replace(
    "onClick={() => alert('Đang phát triển PHASE 4: Thêm người dùng')}",
    "onClick={handleOpenAddModal}"
)

# Add Modal
content = content.replace(
    "    </div>\n  );\n}",
    """
      {/* Modal Thêm/Sửa */}
      <UserFormModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        user={editUser}
        onSuccess={() => {
          fetchUsers();
          fetchStats();
        }}
      />
    </div>
  );
}"""
)

# Also pass onEdit to UserDetailPanel
content = content.replace(
    "<UserDetailPanel \n              user={selectedUser} \n              onClose={() => setSelectedUser(null)} \n            />",
    "<UserDetailPanel \n              user={selectedUser} \n              onClose={() => setSelectedUser(null)} \n              onEdit={(u) => { setEditUser(u); setIsModalOpen(true); }}\n            />"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx for Phase 4")
