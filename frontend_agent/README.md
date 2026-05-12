## 📋 Что сделано

1. **Структура папок** — создаём `src/` с папками `pages/` (страницы), `components/` (переиспользуемые компоненты), `store/` (хранилище состояния), `api/` (запросы к бэкенду), `types/` (TypeScript типы), `hooks/` (пользовательские хуки) — это стандартная архитектура Feature-based для React-приложений

2. **Роутинг** — React Router v6 управляет навигацией между страницами: `/` главная, `/product/:id` товар, `/cart` корзина, `/checkout` оформление, `/account` личный кабинет, `/auth` вход/регистрация

3. **Хранилище состояния** — Zustand разделён на три стора: `cartStore` (товары в корзине), `userStore` (данные пользователя и JWT токен), `bonusStore` (баланс бонусов и история) — они независимы и подключаются только там, где нужны

4. **API-слой** — `api/client.ts` создаёт Axios-инстанс с базовым URL бэкенда и автоматической подстановкой JWT токена в заголовки, отдельные файлы `api/bouquets.ts`, `api/orders.ts`, `api/auth.ts` группируют запросы по сущностям

5. **Компоненты** — `Header` с балансом бонусов и счётчиком корзины, `ProductCard` для каталога, `BonusWidget` с прогресс-баром уровней лояльности, `PaymentForm` с встроенным виджетом ЮKassa, `OrderHistory` с историей заказов

6. **Валидация форм** — React Hook Form + Zod схемы в каждой форме (регистрация, доставка, оплата) — Zod описывает правила, React Hook Form управляет состоянием полей и показывает ошибки

7. **Интеграция ЮKassa** — `PaymentForm` динамически загружает скрипт `checkout.js` от ЮKassa и рендерит платёжный виджет в div на странице, токен подтверждения приходит с бэкенда

8. **Бонусная система в UI** — логика уровней (Стандарт/Серебро/Золото) вынесена в `hooks/useLoyalty.ts`, компонент `LoyaltyProgress` показывает прогресс-бар до следующего уровня, в корзине ползунок для списания баллов

9. **Тема и стили** — Tailwind CSS настроен с кастомной палитрой: розовый `#F9A8D4`, зелёный `#86EFAC`, кремовый `#FDF2F8` — все компоненты используют эти цвета для единого цветочного стиля

10. **Зависимости между файлами** — `main.tsx` → `App.tsx` (роутер) → страницы → компоненты → сторы/хуки/API — данные текут сверху вниз, изменения состояния через сторы Zustand

---

## 🗂 Структура проекта

---

## 📦 package.json и конфиг

---

## 🔷 TypeScript типы

---

## 🌐 API слой

---

## 🗃 Zustand сторы

---

## 🪝 Хуки

---

## 🧩 Компоненты UI

```typescript
// src/components/ui/Badge.tsx
import React from 'react';
import clsx from 'clsx';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'rose' | 'sage' | 'gold' | 'gray';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'rose',
  className,
}) => {
  const variants = {
    rose: 'bg-rose-100 text-rose-700 border border-rose-200',
    sage: 'bg-sage-100 text-sage-700 border border-sage-200',
    gold: 'bg-amber-100 text-amber-700 border border-amber-200',
    gray: 'bg-gray-100 text-gray-600 border border-gray-200',
  };

---
## 📁 Созданные файлы
- [requirements-2.txt](requirements-2.txt)
- [package.json](package.json)
- [tailwind.config.ts](tailwind.config.ts)
- [index.ts](index.ts)
- [client.ts](client.ts)
- [bouquets.ts](bouquets.ts)
- [auth.ts](auth.ts)
- [orders.ts](orders.ts)
- [cartStore.ts](cartStore.ts)
- [userStore.ts](userStore.ts)
- [bonusStore.ts](bonusStore.ts)
- [useLoyalty.ts](useLoyalty.ts)
- [useYooKassa.ts](useYooKassa.ts)
- [Button.tsx](Button.tsx)