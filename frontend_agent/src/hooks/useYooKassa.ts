import { useEffect, useRef, useCallback } from 'react';

declare global {
  interface Window {
    YooMoneyCheckoutWidget: new (config: YooKassaConfig) => YooKassaWidget;
  }
}

interface YooKassaConfig {
  confirmation_token: string;
  return_url: string;
  amount?: {
    value: string;
    currency: string;
  };
  customization?: {
    colors?: {
      control_primary?: string;
    };
  };
  error_callback?: (error: any) => void;
}

interface YooKassaWidget {
  render: (elementId: string) => void;
  destroy: () => void;
}

interface UseYooKassaOptions {
  confirmationToken: string;
  returnUrl: string;
  amount: number;
  onError?: (error: any) => void;
}

export const useYooKassa = ({
  confirmationToken,
  returnUrl,
  amount,
  onError,
}: UseYooKassaOptions) => {
  const widgetRef = useRef<YooKassaWidget | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const loadScript = useCallback((): Promise<void> => {
    return new Promise((resolve, reject) => {
      if (document.querySelector('script[src*="yookassa"]')) {
        resolve();
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://yookassa.ru/checkout-widget/v1/checkout-widget.js';
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Не удалось загрузить виджет ЮKassa'));
      document.head.appendChild(script);
    });
  }, []);

  const initWidget = useCallback(async () => {
    if (!confirmationToken || !containerRef.current) return;

    try {
      await loadScript();

      if (widgetRef.current) {
        widgetRef.current.destroy();
      }

      widgetRef.current = new window.YooMoneyCheckoutWidget({
        confirmation_token: confirmationToken,
        return_url: returnUrl,
        amount: {
          value: amount.toFixed(2),
          currency: 'RUB',
        },
        customization: {
          colors: {
            control_primary: '#EC4899',
          },
        },
        error_callback: onError,
      });

      widgetRef.current.render('yookassa-container');
    } catch (error) {
      console.error('Ошибка инициализации ЮKassa:', error);
      onError?.(error);
    }
  }, [confirmationToken, returnUrl, amount, loadScript, onError]);

  useEffect(() => {
    initWidget();
    return () => {
      widgetRef.current?.destroy();
    };
  }, [initWidget]);

  return { containerRef };
};