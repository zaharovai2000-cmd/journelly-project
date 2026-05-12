# Лендинг цветов

# Анализ проекта и подготовка к публикации

## Что публикуется

Полноценный веб-сервис для онлайн-продажи букетов цветов, состоящий из **трёх основных частей**:

| Компонент | Стек | Назначение |
|---|---|---|
| `backend_agent` | Python / FastAPI | REST API, бизнес-логика, БД |
| `frontend_agent` | Next.js / Tailwind CSS | Клиентский лендинг и ЛК |
| `ba_agent` | — | Аналитика / документация проекта |

---

## ⚠️ Перед публикацией — обязательно проверить

```bash
# Найти потенциальные секреты в config.py
grep -E "(SECRET|TOKEN|PASSWORD|API_KEY|YOOMONEY)" backend_agent/app/core/config.py
```

> Файл `config.py` **наиболее вероятно содержит** токены ЮMoney, секрет JWT,  
> строку подключения к БД — **всё это должно быть в `.env`, не в коде**

---

## README — сводка для публикации

```markdown
# 🌸 FlowerShop — онлайн-лендинг для продажи букетов

Полнофункциональный интернет-магазин букетов цветов с интеграцией онлайн-кассы
через платёжную систему **ЮMoney** (Яндекс.Деньги). Покупатель может оформить заказ
прямо на сайте, оплатить онлайн и получить фискальный чек. Поддерживается каталог
букетов с фильтрацией, корзина и оформление заказа в несколько шагов.

Пользователи могут зарегистрироваться и войти в **личный кабинет**, где доступна
история заказов, управление профилем и **бонусная программа** — баллы начисляются
за каждую покупку и могут быть использованы как скидка при следующем заказе.
Аутентификация реализована через JWT-токены.

Проект построен на связке **FastAPI** (бэкенд, PostgreSQL через SQLAlchemy) и
**Next.js + Tailwind CSS** (фронтенд). Готов к развёртыванию через Docker Compose.
Конфигурация чувствительных данных вынесена в `.env`-файл и **не хранится в репозитории**.
```

---

## Структура для публикации

```
flower-shop/
├── .env.example          # ← создать (шаблон без секретов)
├── .gitignore            # ← создать
├── docker-compose.yml    # ← создать
├── README.md             # ← итоговый
├── ba_agent/
│   └── README.md
├── backend_agent/
│   ├── Dockerfile        # ← создать
│   ├── requirements.txt
│   └── app/
│       ├── core/
│       │   ├── config.py      # ⚠️ очистить секреты
│       │   ├── database.py
│       │   ├── security.py
│       │   └── dependencies.py
│       ├── models/
│       ├── schemas/
│       └── ...
└── frontend_agent/
    ├── Dockerfile        # ← создать
    ├── package.json
    └── src/
```

---

## .env.example (создать этот файл)

```env
# База данных
DATABASE_URL=postgresql://user:password@db:5432/flowerdb

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ЮMoney
YOOMONEY_SHOP_ID=your-shop-id
YOOMONEY_SECRET_KEY=your-yoomoney-secret
YOOMONEY_RETURN_URL=https://yourdomain.ru/payment/success

# Общее
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.ru
```

---

## Commit-сообщение

```
feat: initial release — flower shop with YooMoney payments & bonus system

- FastAPI backend: auth (JWT), orders, payments, bonus points
- Next.js frontend: landing, catalog, cart, personal account
- YooMoney online checkout integration
- Bonus accumulation system for registered users
- Project structure prepared for Docker Compose deployment
- Secrets moved to .env.example (no credentials in repo)
```

---

> **Итог:** проект готов к публикации **после** выноса секретов в `.env` и создания  
> `.gitignore`, `.env.example`, `Dockerfile` × 2, `docker-compose.yml`  
> Хотите — сгенерирую эти файлы?

---
*Сгенерировано Journelly Dev System*