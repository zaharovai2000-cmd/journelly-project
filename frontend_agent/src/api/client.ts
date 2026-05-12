import axios from 'axios';
import { useUserStore } from '../store/userStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Подставляем JWT токен в каждый запрос
apiClient.interceptors.request.use((config) => {
  const token = useUserStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Обрабатываем истёкший токен
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      useUserStore.getState().logout();
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);