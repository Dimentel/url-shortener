# URL Shortener Service

Сервис для сокращения URL-адресов с возможностью аутентификации, статистикой переходов и управлением ссылками.

## 📄 Описание API

### Основные возможности:
- **Создание коротких ссылок** (доступно без авторизации).
- **Перенаправление** по коротким ссылкам.
- **Статистика переходов**: количество кликов, дата создания, последнее использование.
- **Аутентификация** (JWT-токены):
  - Регистрация/логин.
  - Защищённые эндпоинты для управления ссылками.
- **Поиск ссылок** по оригинальному URL.

![Корневой эндпоинт (часть 1)](screens/01 Корневой запрос часть 1.PNG)
![Корневой эндпоинт (часть 2)](screens/02 Корневой запрос часть 2.PNG)

---

## 🗃️ Описание БД

### Таблицы:
1. **users** (пользователи):
   - `id` (UUID)
   - `email` (уникальный)
   - `hashed_password`
   - `is_active` (флаг)

2. **links** (ссылки):
   - `id` (автоинкремент)
   - `original_url`
   - `short_code` (уникальный)
   - `created_at`
   - `expires_at`
   - `user_id` (связь с users.id)
   - `clicks` (счётчик переходов)
   - `last_used_at`

![Миграции](screens/03 Создание таблиц базы данных миграцией.PNG)

---

## 🚀 Инструкция по запуску

### Требования:
- Docker
- Docker Compose

### Шаги:
1. Склонируйте репозиторий:
   bash
   git clone https://github.com/Dimentel/url-shortener.git
   cd url-shortener
2. Создайте файл `.env` в корне проекта:
ini
*Настройки JWT*
JWT_LOGIN_EXPIRES_IN=3600
JWT_SECRET=ваш_секретный_ключ

*Настройки SMTP (для отправки email)*
SMTP_USER=ваш_email@example.com
SMTP_PASSWORD=ваш_пароль
SMTP_HOST=smtp.example.com
SMTP_PORT=465

*Настройки PostgreSQL*
DB_USER=user
DB_PASS=password
DB_HOST=db
DB_PORT=5432
DB_NAME=dbname

Замените ваш_секретный_ключ, ваш_email@example.com и другие значения на реальные данные.
3. Соберите и запустите контейнеры
docker-compose up --build
После запуска API будет доступен по адресу:
http://localhost:8000
Документация Swagger: http://localhost:8000/docs
## 📋 Примеры запросов

### 1. **Незащищённый эндпоинт**
- **GET /unprotected-route**  
  Возвращает сообщение для неавторизованных пользователей.  
  ![Незащищённый эндпойнт](screens/04 GET unprotected-route.PNG)

---

### 2. **Аутентификация**
- **POST /auth/register**  
  ![Регистрация пользователя](screens/05 POST регистрация.PNG)
- **POST /auth/jwt/login**  
  ![Login](screens/06 Login.PNG)
  - **POST /auth/jwt/logout**  
  ![Logout](screens/07 Logout.PNG)
### 3. **Защищённый эндпоинт**
- **GET /protected-route**  
  Возвращает сообщение для авторизованных пользователей.  
  ![Защищённый эндпойнт](screens/08 GET protected-route.PNG)

---
### 4. **Работа со ссылками**
- **POST /links/shorten**  
  Создание ссылок для авторизованных пользователей.  
  ![Создание ссылки авторизованный](screens/09 POST links-shorten авторизованный.PNG)
- **POST /links/shorten/anonymous**  
  Создание ссылок для авторизованных пользователей.  
  ![Создание ссылки НЕавторизованный](screens/10 POST links-shorten НЕавторизованный.PNG)
- **GET /links/search**  
  Поиск короткой ссылки по оригинальному url.  
  ![Поиск сссылки](screens/11 GET links-search.PNG)
- **GET /links/{short_link}**  
  Переход на оригинальный url по короткой ссылке.  
  ![ввод короткой ссылки](screens/12 GET переход по короткой ссылке ввод адреса.PNG)
  ![переадресация](screens/13 GET переход по короткой ссылке после перехода.PNG)
- **GET /links/{short_link}/stats**  
  Просмотр статистики о короткой ссылке.  
  ![Поиск сссылки](screens/14 GET Статистика.PNG)
- **PUT /links/{short_link}**  
  Изменение короткой ссылки.  
  ![Поиск сссылки](screens/15 PUT изменение ссылки.PNG)
- **DELETE /links/{short_link}**  
  Удаление короткой ссылки.  
  ![Поиск сссылки](screens/16 DELETE удаление ссылки.PNG)
---