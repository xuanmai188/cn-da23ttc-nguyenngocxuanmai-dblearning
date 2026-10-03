import axiosClient from './axiosClient';

export const recommendationApi = {

  // Dynamic Survey
  getActiveSurvey: () => axiosClient.get('/survey/active'),
  skipOnboarding: () => axiosClient.post('/survey/skip'),
  submitSurvey: (surveyId, data) => axiosClient.post(`/survey/${surveyId}/submit`, data),

  getRecommendations: () => axiosClient.get('/recommendations/'),
  getProfile: () => axiosClient.get('/recommendations/profile'),
  submitOnboarding: (data) => axiosClient.post('/recommendations/onboarding', data)
};
