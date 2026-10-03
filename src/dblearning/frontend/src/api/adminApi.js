import axiosClient from './axiosClient';

export const adminApi = {

  // Surveys
  getSurveys: () => axiosClient.get('/admin/surveys'),

  getSurveyStats: () => axiosClient.get('/admin/surveys/stats/overview'),
  getSurveyResults: () => axiosClient.get('/admin/surveys/active/results'),

  createSurvey: (data) => axiosClient.post('/admin/surveys', data),
  updateSurvey: (id, data) => axiosClient.put(`/admin/surveys/${id}`, data),
  deleteSurvey: (id) => axiosClient.delete(`/admin/surveys/${id}`),
  activateSurvey: (id) => axiosClient.post(`/admin/surveys/${id}/activate`),
  
  // Survey Questions
  getSurveyQuestions: (surveyId) => axiosClient.get(`/admin/surveys/${surveyId}/questions`),
  createSurveyQuestion: (surveyId, data) => axiosClient.post(`/admin/surveys/${surveyId}/questions`, data),
  deleteSurveyQuestion: (questionId) => axiosClient.delete(`/admin/questions/${questionId}`),

  getDashboardStats: () => axiosClient.get('/admin/dashboard'),
  getFullStatistics: () => axiosClient.get('/admin/statistics/full'),

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
  
  // Learning Items
  getItems: (params) => axiosClient.get('/admin/items', { params }),
  createItem: (data) => axiosClient.post('/admin/items', data),
  updateItem: (id, data) => axiosClient.put(`/admin/items/${id}`, data),
  deleteItem: (id) => axiosClient.delete(`/admin/items/${id}`),
  
  // Quizzes
  getQuizzes: (params) => axiosClient.get('/admin/quizzes', { params }),
  createQuiz: (data) => axiosClient.post('/admin/quizzes', data),
  updateQuiz: (id, data) => axiosClient.put(`/admin/quizzes/${id}`, data),
  deleteQuiz: (id) => axiosClient.delete(`/admin/quizzes/${id}`),
  
  // Questions
  getQuestionsByQuiz: (quizId) => axiosClient.get(`/admin/quizzes/${quizId}/questions`),
  createQuestion: (quizId, data) => axiosClient.post(`/admin/quizzes/${quizId}/questions`, data),
  updateQuestion: (id, data) => axiosClient.put(`/admin/questions/${id}`, data),
  deleteQuestion: (id) => axiosClient.delete(`/admin/questions/${id}`),
  
  // Flashcards
  getFlashcardsByItem: (itemId) => axiosClient.get(`/admin/items/${itemId}/flashcards`),
  createFlashcard: (itemId, data) => axiosClient.post(`/admin/items/${itemId}/flashcards`, data),
  updateFlashcard: (id, data) => axiosClient.put(`/admin/flashcards/${id}`, data),
  deleteFlashcard: (id) => axiosClient.delete(`/admin/flashcards/${id}`),
  
  // Charts & Stats
  getUserGrowthChart: () => axiosClient.get('/admin/charts/user-growth'),
  getActivityChart: () => axiosClient.get('/admin/charts/activity'),
  getTopicLearningChart: () => axiosClient.get('/admin/charts/topic-learning'),
  getPerformanceStats: () => axiosClient.get('/admin/performance'),
  getActiveStudents: () => axiosClient.get('/admin/active-students'),
  getPopularLessons: () => axiosClient.get('/admin/popular-lessons'),
  getRecentActivities: (limit = 5) => axiosClient.get(`/admin/recent-activities?limit=${limit}`),
  
  // Notifications
  getNotifications: () => axiosClient.get('/admin/notifications'),
  markAllNotificationsRead: () => axiosClient.put('/admin/notifications/read-all'),
  markNotificationRead: (id) => axiosClient.put(`/admin/notifications/${id}/read`),
};
