file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
content = """import axiosClient from './axiosClient';

export const adminApi = {
  getDashboardStats: () => axiosClient.get('/admin/dashboard'),
  getUsers: () => axiosClient.get('/admin/users'),
  toggleUserStatus: (userId) => axiosClient.put(`/admin/users/${userId}/status`),
  toggleUserRole: (userId) => axiosClient.put(`/admin/users/${userId}/role`)
};
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("adminApi.js written")
