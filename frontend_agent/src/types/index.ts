export interface Bouquet {
  id: string;
  name: string;
  description: string;
  price: number;
  images: string[];
  category: BouquetCategory;
  size: BouquetSize;
  occasion: string[];
  colors: string[];
  composition: string;
  inStock: boolean;
  isHit: boolean;
  isNew: boolean;
  bonusPoints: number; // сколько бонусов начислится
}

export type BouquetCategory = 'roses' | 'mixed' | 'seasonal' | 'wedding' | 'exotic';
export type BouquetSize = 'small' | 'medium' | 'large';

export interface CartItem {
  bouquet: Bouquet;
  quantity: number;
  selectedSize: BouquetSize;
}

export interface User {
  id: string;
  name: string;
  phone: string;
  email: string;
  birthDate?: string;
  createdAt: string;
}

export interface BonusTransaction {
  id: string;
  type: 'accrual' | 'debit';
  amount: number;
  description: string;
  orderId?: string;
  createdAt: string;
}

export interface BonusAccount {
  balance: number;
  totalEarned: number;
  level: LoyaltyLevel;
  transactions: BonusTransaction[];
}

export type LoyaltyLevel = 'standard' | 'silver' | 'gold';

export interface LoyaltyConfig {
  level: LoyaltyLevel;
  label: string;
  minPoints: number;
  maxPoints: number;
  color: string;
  icon: string;
  discount: number; // процент кешбэка
}

export interface Order {
  id: string;
  orderNumber: string;
  status: OrderStatus;
  items: OrderItem[];
  deliveryAddress: DeliveryAddress;
  deliveryDate: string;
  deliveryTime: string;
  totalAmount: number;
  bonusUsed: number;
  bonusEarned: number;
  paymentMethod: 'online' | 'cash';
  paymentStatus: 'pending' | 'paid' | 'failed';
  createdAt: string;
  giftMessage?: string;
}

export type OrderStatus = 'new' | 'confirmed' | 'preparing' | 'delivering' | 'delivered' | 'cancelled';

export interface OrderItem {
  bouquetId: string;
  bouquetName: string;
  bouquetImage: string;
  quantity: number;
  price: number;
  size: BouquetSize;
}

export interface DeliveryAddress {
  city: string;
  street: string;
  house: string;
  apartment?: string;
  comment?: string;
}

export interface PaymentIntent {
  paymentId: string;
  confirmationToken: string;
  amount: number;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}