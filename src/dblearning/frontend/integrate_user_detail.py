file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Import UserDetailPanel
content = content.replace(
    "import UserTable from '../../components/admin/users/UserTable';",
    "import UserTable from '../../components/admin/users/UserTable';\nimport UserDetailPanel from '../../components/admin/users/UserDetailPanel';"
)

# Add selectedUser state
content = content.replace(
    "const [error, setError] = useState('');",
    "const [error, setError] = useState('');\n  const [selectedUser, setSelectedUser] = useState(null);"
)

# Modify handleAction
new_handle_action = """const handleAction = (type, user) => {
    if (type === 'view') {
      setSelectedUser(user);
    } else if (type === 'edit') {
      alert(`Đang phát triển PHASE 4: Chỉnh sửa ${user.full_name}`);
    } else if (type === 'more') {
      alert(`Menu thao tác cho ${user.full_name}`);
    }
  };"""
content = content.replace(
    """const handleAction = (type, user) => {
    if (type === 'view') {
      alert(`Đang phát triển PHASE 3: Xem chi tiết ${user.full_name}`);
    } else if (type === 'edit') {
      alert(`Đang phát triển PHASE 4: Chỉnh sửa ${user.full_name}`);
    } else if (type === 'more') {
      alert(`Menu thao tác cho ${user.full_name}`);
    }
  };""",
    new_handle_action
)

# Render UserDetailPanel
content = content.replace(
    "    </div>\n  );\n}",
    """
      {/* Detail Panel */}
      {selectedUser && (
        <UserDetailPanel 
          user={selectedUser} 
          onClose={() => setSelectedUser(null)} 
        />
      )}
    </div>
  );
}"""
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserManagement.jsx with UserDetailPanel")
