file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """  resetUserPassword: (id) => axiosClient.put(`/admin/users/${id}/reset-password`),
  
  // Notifications
  getNotifications: () => axiosClient.get('/admin/notifications'),
  markAllNotificationsRead: () => axiosClient.put('/admin/notifications/read-all'),
  markNotificationRead: (id) => axiosClient.put(`/admin/notifications/${id}/read`),"""

content = content.replace(
    "resetUserPassword: (id) => axiosClient.put(`/admin/users/${id}/reset-password`),",
    new_endpoints
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js")
