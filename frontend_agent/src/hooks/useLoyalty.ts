import { LoyaltyConfig, LoyaltyLevel } from '../types';

const LOYALTY_CONFIGS: Record<LoyaltyLevel, LoyaltyConfig> = {
  standard: {
    level: 'standard',
    label: 'Стандарт',
    minPoints: 0,
    maxPoints: 999,
    color: 'from-gray-400 to-gray-500',
    icon: '🌸',
    discount: 5,
  },
  silver: {
    level: 'silver',
    label: 'Серебро',
    minPoints: 1000,
    maxPoints: 4999,
    color: 'from-slate-400 to-slate-500',
    icon: '🥈',
    discount: 7,
  },
  gold: {
    level: 'gold',
    label: 'Золото',
    minPoints: 5000,
    maxPoints: Infinity,
    color: 'from-yellow-400 to-amber-500',
    icon: '🥇',
    discount: 10,
  },
};

export const useLoyalty = () => {
  const getConfig = (level: LoyaltyLevel): LoyaltyConfig => LOYALTY_CONFIGS[level];
  const getAllConfigs = () => Object.values(LOYALTY_CONFIGS);

  return { getConfig, getAllConfigs, LOYALTY_CONFIGS };
};