file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = "  getFullStatistics: () => axiosClient.get('/admin/statistics/full'),\n"
if "getFullStatistics" not in content:
    content = content.replace(
        "  getDashboardStats: () => axiosClient.get('/admin/dashboard'),",
        "  getDashboardStats: () => axiosClient.get('/admin/dashboard'),\n" + new_endpoint
    )

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added getFullStatistics to adminApi.js")
