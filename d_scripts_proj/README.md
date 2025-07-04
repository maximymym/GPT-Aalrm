## 🚀 Инструкции по развертыванию

### 🚀 Начало работы

#### 1. Настройте переменные окружения

Создайте файл `.env` в корне проекта, скопировав файл-пример:
```shell
cp .env.example .env
```
Затем отредактируйте `.env`, указав свои значения, особенно `SECRET_KEY` и `BOT_TOKEN`.

#### 2. Создайте суперпользователя Django

Чтобы войти в систему через Telegram-бот, вам понадобится учетная запись администратора Django. Запустите бэкенд-сервис отдельно, чтобы создать ее:
```shell
docker-compose up -d db backend
docker-compose exec backend python manage.py createsuperuser
```
Следуйте инструкциям, чтобы создать своего администратора.

#### 3. Запустите все сервисы

Теперь вы можете запустить весь стек:
```shell
docker-compose up --build -d
```
Сервисы будут доступны по следующим адресам:
-   Веб-сайт: [http://localhost](http://localhost)
-   API бэкенда: [http://localhost/api/](http://localhost/api/)

#### 4. Взаимодействие с ботом

Найдите своего бота в Telegram и используйте команду `/login`, чтобы войти с учетными данными суперпользователя, которые вы создали на шаге 2.
```
/login ваш_username ваш_пароль
```
После входа вы сможете использовать команду `/addscript` для добавления новых скриптов в каталог.
