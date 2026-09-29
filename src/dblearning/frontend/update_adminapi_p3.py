file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "getUserStats: () => axiosClient.get('/admin/users/stats')",
    "getUserStats: () => axiosClient.get('/admin/users/stats'),\n  getUserDetails: (id) => axiosClient.get(`/admin/users/${id}/details`),\n  getUserHistory: (id) => axiosClient.get(`/admin/users/${id}/history`)"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js with getUserDetails and getUserHistory")
