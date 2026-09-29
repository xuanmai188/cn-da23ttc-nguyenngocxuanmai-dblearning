file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("toggleUserRole: (userId) => axiosClient.put(`/admin/users/${userId}/role`)\n  getUserGrowthChart", "toggleUserRole: (userId) => axiosClient.put(`/admin/users/${userId}/role`),\n  getUserGrowthChart")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("adminApi.js comma fixed")
