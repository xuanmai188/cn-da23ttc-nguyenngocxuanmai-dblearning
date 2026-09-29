import axiosClient from './axiosClient';

export const recommendationApi = {
  getRecommendations: () => axiosClient.get('/recommendations/'),
  getProfile: () => axiosClient.get('/recommendations/profile'),
  submitOnboarding: (data) => axiosClient.post('/recommendations/onboarding', data)
};
