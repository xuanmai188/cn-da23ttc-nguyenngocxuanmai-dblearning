file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("getRecentActivities: () => axiosClient.get('/admin/recent-activities'),", "getRecentActivities: (limit = 5) => axiosClient.get(`/admin/recent-activities?limit=${limit}`),")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js")
