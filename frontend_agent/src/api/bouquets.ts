import { apiClient } from './client';
import { Bouquet } from '../types';

export interface BouquetsFilter {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  size?: string;
  occasion?: string;
  page?: number;
  limit?: number;
}

export const bouquetsApi = {
  getAll: async (filters?: BouquetsFilter): Promise<{ items: Bouquet[]; total: number }> => {
    const { data } = await apiClient.get('/bouquets', { params: filters });
    return data;
  },

  getById: async (id: string): Promise<Bouquet> => {
    const { data } = await apiClient.get(`/bouquets/${id}`);
    return data;
  },

  getHits: async (): Promise<Bouquet[]> => {
    const { data } = await apiClient.get('/bouquets?is_hit=true&limit=6');
    return data.items;
  },
};