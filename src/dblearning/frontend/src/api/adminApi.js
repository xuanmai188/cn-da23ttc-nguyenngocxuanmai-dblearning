import axiosClient from './axiosClient';

export const adminApi = {
  getDashboardStats: () => axiosClient.get('/admin/dashboard'),
  getUsers: (params) => axiosClient.get('/admin/users', { params }),
  getUserStats: () => axiosClient.get('/admin/users/stats'),
  getUserDetails: (id) => axiosClient.get(`/admin/users/${id}/details`),
  getUserHistory: (id) => axiosClient.get(`/admin/users/${id}/history`),
  toggleUserStatus: (userId) => axiosClient.put(`/admin/users/${userId}/status`),
  toggleUserRole: (userId) => axiosClient.put(`/admin/users/${userId}/role`),
  getUserGrowthChart: () => axiosClient.get('/admin/charts/user-growth'),
  getActivityChart: () => axiosClient.get('/admin/charts/activity'),
  getTopics: () => axiosClient.get('/admin/topics'),
  createTopic: (data) => axiosClient.post('/admin/topics', data),
  updateTopic: (id, data) => axiosClient.put(`/admin/topics/${id}`, data),
  deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`),
  getTopicLearningChart: () => axiosClient.get('/admin/charts/topic-learning'),
  getPerformanceStats: () => axiosClient.get('/admin/performance'),
  getActiveStudents: () => axiosClient.get('/admin/active-students'),
  getPopularLessons: () => axiosClient.get('/admin/popular-lessons'),
  getRecentActivities: () => axiosClient.get('/admin/recent-activities'),
};
