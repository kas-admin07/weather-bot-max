# 🌤 MAX Weather Bot

Погодный бот для платформы MAX с интеграцией через Netlify Functions.

## 📋 Описание

Это Telegram-бот, который предоставляет актуальную информацию о погоде для любого города мира. Бот интегрирован с платформой MAX и развернут на Netlify для обеспечения высокой доступности и масштабируемости.

## ✨ Возможности

- 🌍 Получение погоды для любого города мира
- 🇷🇺 Полная поддержка русского языка
- ⚡ Быстрые ответы через Netlify Functions
- 🔄 Автоматическая обработка вебхуков MAX API
- 📱 Удобный интерфейс с HTML-разметкой
- 🛡️ Надежная обработка ошибок

## 🏗️ Архитектура проекта

```
weather-bot-max/
├── bot/
│   ├── __init__.py          # Инициализация пакета
│   └── weather.py           # Модуль получения погоды
├── netlify/
│   └── functions/
│       ├── app.py           # Главная функция
│       ├── health.py        # Health check
│       └── webhook.py       # Обработчик вебхуков
├── netlify.toml             # Конфигурация Netlify
├── requirements.txt         # Зависимости Python
├── runtime.txt              # Версия Python
└── README.md               # Документация
```

## 🚀 Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/kas-admin07/weather-bot-max.git
cd weather-bot-max
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
MAX_API_TOKEN=your_max_api_token_here
```

### 4. Локальное тестирование

```bash
# Тестирование модуля погоды
python -c "from bot.weather import get_weather_info; print(get_weather_info('Москва'))"

# Тестирование вебхука
python netlify/functions/webhook.py
```

## 🌐 Деплой на Netlify

### Автоматический деплой

1. Подключите репозиторий к Netlify
2. Настройте переменные окружения в Netlify:
   - `MAX_API_TOKEN` - токен MAX API
3. Деплой произойдет автоматически при пуше в main ветку

### Ручной деплой

```bash
# Установка Netlify CLI
npm install -g netlify-cli

# Логин в Netlify
netlify login

# Деплой
netlify deploy --prod
```

## 📡 API Endpoints

### Основные эндпоинты

- `GET /` - Информация о боте
- `POST /webhook/max` - Обработка вебхуков от MAX API
- `GET /health` - Проверка состояния сервера

### Примеры запросов

#### Проверка состояния
```bash
curl https://your-netlify-app.netlify.app/health
```

#### Информация о боте
```bash
curl https://your-netlify-app.netlify.app/
```

## 🤖 Команды бота

- `/start` - Приветствие и инструкции
- `/help` - Справка по использованию
- `Название города` - Получение погоды

### Примеры использования

```
Пользователь: Москва
Бот: 🌤 Погода в городе Москва:
     ⛅️ +5°C

Пользователь: London
Бот: 🌤 Погода в городе London:
     🌧 +12°C
```

## 🔧 Конфигурация

### netlify.toml

```toml
[build]
  command = "pip install -r requirements.txt"
  functions = "netlify/functions"

[build.environment]
  PYTHON_VERSION = "3.10"

[[redirects]]
  from = "/webhook/max"
  to = "/.netlify/functions/webhook"
  status = 200

[[redirects]]
  from = "/health"
  to = "/.netlify/functions/health"
  status = 200

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/app"
  status = 200
```

### requirements.txt

```
requests==2.31.0
python-dotenv==1.0.0
Flask==2.3.3
```

## 🛠️ Разработка

### Структура кода

- **bot/weather.py** - Основная логика получения погоды
- **netlify/functions/webhook.py** - Обработка вебхуков MAX API
- **netlify/functions/health.py** - Health check эндпоинт
- **netlify/functions/app.py** - Главная страница API

### Добавление новых функций

1. Создайте новую функцию в `netlify/functions/`
2. Добавьте соответствующий redirect в `netlify.toml`
3. Обновите документацию

### Тестирование

```bash
# Тест модуля погоды
python -m pytest tests/ -v

# Локальный запуск функций
netlify dev
```

## 🔒 Безопасность

- Все API токены хранятся в переменных окружения
- Валидация входящих данных
- Обработка ошибок и исключений
- Логирование всех операций

## 📊 Мониторинг

### Логи

Все операции логируются с соответствующими уровнями:
- `INFO` - Обычные операции
- `WARNING` - Предупреждения
- `ERROR` - Ошибки

### Health Check

Используйте эндпоинт `/health` для мониторинга состояния:

```json
{
  "status": "healthy",
  "service": "MAX Weather Bot",
  "version": "1.0.0",
  "timestamp": "request_id"
}
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/kas-admin07/weather-bot-max/issues)
2. Создайте новый Issue с подробным описанием
3. Используйте теги для категоризации проблемы

## 🔄 Обновления

### v1.0.0
- Базовая функциональность получения погоды
- Интеграция с MAX API
- Деплой на Netlify
- Полная документация

---

**Создано с ❤️ для платформы MAX**