file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace getUsers
content = content.replace(
    "getUsers: () => axiosClient.get('/admin/users'),",
    "getUsers: (params) => axiosClient.get('/admin/users', { params }),\n  getUserStats: () => axiosClient.get('/admin/users/stats'),"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js with getUserStats and paginated getUsers")
