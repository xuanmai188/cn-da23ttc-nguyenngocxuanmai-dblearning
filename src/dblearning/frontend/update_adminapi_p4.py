file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "toggleUserRole: (id) => axiosClient.put(`/admin/users/${id}/role`),",
    "toggleUserRole: (id) => axiosClient.put(`/admin/users/${id}/role`),\n  createUser: (data) => axiosClient.post('/admin/users', data),\n  updateUser: (id, data) => axiosClient.put(`/admin/users/${id}`, data),\n  resetUserPassword: (id) => axiosClient.put(`/admin/users/${id}/reset-password`),"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js with Phase 4 APIs")
