import { create } from 'zustand';
import { BonusTransaction, LoyaltyLevel } from '../types';

interface BonusStore {
  balance: number;
  totalEarned: number;
  transactions: BonusTransaction[];
  isLoading: boolean;

  setBalance: (balance: number, totalEarned: number) => void;
  setTransactions: (transactions: BonusTransaction[]) => void;
  addTransaction: (transaction: BonusTransaction) => void;
  setLoading: (loading: boolean) => void;

  getLoyaltyLevel: () => LoyaltyLevel;
  getNextLevelProgress: () => number;
  getNextLevelTarget: () => number;
}

export const useBonusStore = create<BonusStore>((set, get) => ({
  balance: 0,
  totalEarned: 0,
  transactions: [],
  isLoading: false,

  setBalance: (balance, totalEarned) => set({ balance, totalEarned }),
  setTransactions: (transactions) => set({ transactions }),
  addTransaction: (transaction) =>
    set((state) => ({ transactions: [transaction, ...state.transactions] })),
  setLoading: (isLoading) => set({ isLoading }),

  getLoyaltyLevel: (): LoyaltyLevel => {
    const { totalEarned } = get();
    if (totalEarned >= 5000) return 'gold';
    if (totalEarned >= 1000) return 'silver';
    return 'standard';
  },

  getNextLevelProgress: () => {
    const { totalEarned } = get();
    if (totalEarned >= 5000) return 100;
    if (totalEarned >= 1000) return ((totalEarned - 1000) / 4000) * 100;
    return (totalEarned / 1000) * 100;
  },

  getNextLevelTarget: () => {
    const { totalEarned } = get();
    if (totalEarned >= 5000) return 5000;
    if (totalEarned >= 1000) return 5000;
    return 1000;
  },
}));