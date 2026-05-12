import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { CartItem, Bouquet, BouquetSize } from '../types';

interface CartStore {
  items: CartItem[];
  bonusToUse: number;

  addItem: (bouquet: Bouquet, size: BouquetSize) => void;
  removeItem: (bouquetId: string) => void;
  updateQuantity: (bouquetId: string, quantity: number) => void;
  setBonusToUse: (amount: number) => void;
  clearCart: () => void;

  // Вычисляемые значения
  getTotalItems: () => number;
  getSubtotal: () => number;
  getDiscount: () => number;
  getTotal: () => number;
  getBonusEarned: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      bonusToUse: 0,

      addItem: (bouquet, size) => {
        set((state) => {
          const existing = state.items.find(
            (item) => item.bouquet.id === bouquet.id && item.selectedSize === size
          );
          if (existing) {
            return {
              items: state.items.map((item) =>
                item.bouquet.id === bouquet.id && item.selectedSize === size
                  ? { ...item, quantity: item.quantity + 1 }
                  : item
              ),
            };
          }
          return {
            items: [...state.items, { bouquet, quantity: 1, selectedSize: size }],
          };
        });
      },

      removeItem: (bouquetId) => {
        set((state) => ({
          items: state.items.filter((item) => item.bouquet.id !== bouquetId),
        }));
      },

      updateQuantity: (bouquetId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(bouquetId);
          return;
        }
        set((state) => ({
          items: state.items.map((item) =>
            item.bouquet.id === bouquetId ? { ...item, quantity } : item
          ),
        }));
      },

      setBonusToUse: (amount) => set({ bonusToUse: amount }),

      clearCart: () => set({ items: [], bonusToUse: 0 }),

      getTotalItems: () => get().items.reduce((sum, item) => sum + item.quantity, 0),

      getSubtotal: () =>
        get().items.reduce((sum, item) => sum + item.bouquet.price * item.quantity, 0),

      getDiscount: () => get().bonusToUse,

      getTotal: () => Math.max(0, get().getSubtotal() - get().bonusToUse),

      getBonusEarned: () => Math.floor(get().getTotal() * 0.05),
    }),
    {
      name: 'flower-cart',
      partialize: (state) => ({ items: state.items }),
    }
  )
);