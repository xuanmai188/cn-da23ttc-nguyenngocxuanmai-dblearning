import axiosClient from './axiosClient';

export const reportApi = {
  getLearningActivity: (params) => axiosClient.get('/admin/reports/learning-activity', { params }),
  getLearningResults: (params) => axiosClient.get('/admin/reports/learning-results', { params }),
  getRecommendations: (params) => axiosClient.get('/admin/reports/recommendations', { params }),
  getSurveys: (params) => axiosClient.get('/admin/reports/surveys', { params })
};
