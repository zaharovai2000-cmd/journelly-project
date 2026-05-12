import { apiClient } from './client';
import { Order, PaymentIntent } from '../types';

export interface CreateOrderData {
  items: Array<{ bouquetId: string; quantity: number; size: string }>;
  deliveryAddress: {
    city: string;
    street: string;
    house: string;
    apartment?: string;
    comment?: string;
  };
  deliveryDate: string;
  deliveryTime: string;
  bonusToUse: number;
  paymentMethod: 'online' | 'cash';
  giftMessage?: string;
  recipientName: string;
  recipientPhone: string;
}

export const ordersApi = {
  create: async (data: CreateOrderData): Promise<Order> => {
    const { data: response } = await apiClient.post('/orders', data);
    return response;
  },

  getAll: async (): Promise<Order[]> => {
    const { data } = await apiClient.get('/orders');
    return data;
  },

  getById: async (id: string): Promise<Order> => {
    const { data } = await apiClient.get(`/orders/${id}`);
    return data;
  },

  createPayment: async (orderId: string): Promise<PaymentIntent> => {
    const { data } = await apiClient.post(`/orders/${orderId}/payment`);
    return data;
  },

  getBonusAccount: async (): Promise<{
    balance: number;
    totalEarned: number;
    transactions: any[];
  }> => {
    const { data } = await apiClient.get('/users/me/bonus');
    return data;
  },
};