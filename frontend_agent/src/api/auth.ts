import { apiClient } from './client';
import { User, AuthTokens } from '../types';

export const authApi = {
  register: async (data: {
    name: string;
    phone: string;
    email: string;
    password: string;
  }): Promise<{ user: User; tokens: AuthTokens }> => {
    const { data: response } = await apiClient.post('/auth/register', data);
    return response;
  },

  login: async (data: {
    email: string;
    password: string;
  }): Promise<{ user: User; tokens: AuthTokens }> => {
    const { data: response } = await apiClient.post('/auth/login', data);
    return response;
  },

  getMe: async (): Promise<User> => {
    const { data } = await apiClient.get('/auth/me');
    return data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const { data: response } = await apiClient.patch('/auth/me', data);
    return response;
  },
};