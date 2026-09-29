import axiosClient from './axiosClient';

export const authApi = {
  login: (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    return axiosClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  
  register: (data) => {
    return axiosClient.post('/auth/register', data);
  },
  
  getMe: () => {
    return axiosClient.get('/auth/me');
  },

  updateProfile: (data) => {
    return axiosClient.put('/auth/me', data);
  },

  forgotPassword: (email) => {
    return axiosClient.post('/auth/forgot-password', { email });
  },

  resetPassword: (token, new_password) => {
    return axiosClient.post('/auth/reset-password', { token, new_password });
  }
};
