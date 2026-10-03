file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I will just replace the entire content to include everything
new_content = """import axiosClient from './axiosClient';

export const adminApi = {
  getDashboardStats: () => axiosClient.get('/admin/dashboard'),
  getUsers: (params) => axiosClient.get('/admin/users', { params }),
  getUserStats: () => axiosClient.get('/admin/users/stats'),
  getUserDetails: (id) => axiosClient.get(`/admin/users/${id}/details`),
  getUserHistory: (id) => axiosClient.get(`/admin/users/${id}/history`),
  createUser: (data) => axiosClient.post('/admin/users', data),
  updateUser: (id, data) => axiosClient.put(`/admin/users/${id}`, data),
  toggleUserStatus: (userId) => axiosClient.put(`/admin/users/${userId}/status`),
  resetUserPassword: (userId) => axiosClient.put(`/admin/users/${userId}/reset-password`),
  
  getTopics: () => axiosClient.get('/admin/topics'),
  createTopic: (data) => axiosClient.post('/admin/topics', data),
  updateTopic: (id, data) => axiosClient.put(`/admin/topics/${id}`, data),
  deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`),
  
  // Charts & Stats
  getUserGrowthChart: () => axiosClient.get('/admin/charts/user-growth'),
  getActivityChart: () => axiosClient.get('/admin/charts/activity'),
  getTopicLearningChart: () => axiosClient.get('/admin/charts/topic-learning'),
  getPerformanceStats: () => axiosClient.get('/admin/performance'),
  getActiveStudents: () => axiosClient.get('/admin/active-students'),
  getPopularLessons: () => axiosClient.get('/admin/popular-lessons'),
  getRecentActivities: () => axiosClient.get('/admin/recent-activities'),
  
  // Notifications
  getNotifications: () => axiosClient.get('/admin/notifications'),
  markAllNotificationsRead: () => axiosClient.put('/admin/notifications/read-all'),
  markNotificationRead: (id) => axiosClient.put(`/admin/notifications/${id}/read`),
};
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Rewrote adminApi.js to include all endpoints")
