# Документация проекта Bright Smile (Стоматологическая клиника)

## Оглавление
1. [Общее описание](#общее-описание)
2. [Структура проекта](#структура-проекта)
3. [Модели данных](#модели-данных)
4. [Маршруты и функции](#маршруты-и-функции)
5. [Аутентификация и авторизация](#аутентификация-и-авторизация)
6. [Система сообщений](#система-сообщений)
7. [Панель администратора](#панель-администратора)

## Общее описание

Bright Smile - это веб-приложение для стоматологической клиники, разработанное на Flask. Система предоставляет следующий функционал:
- Регистрация и авторизация пользователей
- Запись на приём к врачу
- Просмотр истории посещений
- Чат с администрацией
- Административная панель управления
- Управление медицинскими картами пациентов

## Структура проекта

```
WeebTest2/
├── app.py              # Основной файл приложения
├── models.py           # Модели данных SQLAlchemy
├── requirements.txt    # Зависимости проекта
├── static/            # Статические файлы (CSS, JS)
├── templates/         # HTML шаблоны
│   ├── admin/        # Шаблоны админ-панели
│   └── ...           # Остальные шаблоны
└── data/             # Директория для данных
    └── users/        # Пользовательские данные
```

## Модели данных

### User (Пользователь)
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
    medical_history = db.Column(JSONEncodedDict)
```

### Appointment (Запись на приём)
```python
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    service_id = db.Column(db.Integer, ForeignKey('service.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
```

### Message (Сообщение)
```python
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    is_from_admin = db.Column(db.Boolean)
    is_read = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
```

### Service (Услуга)
```python
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)
```

## Маршруты и функции

### Публичные маршруты

#### Главная страница (/)
```python
@app.route('/')
def home():
    return render_template('index.html')
```
Отображает главную страницу сайта.

#### Регистрация (/register)
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Обработка регистрации пользователя
```
- GET: Отображает форму регистрации
- POST: Обрабатывает данные регистрации
- Валидирует данные
- Создаёт нового пользователя
- Перенаправляет на страницу входа

#### Вход (/login)
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Обработка входа пользователя
```
- Проверяет учетные данные
- Создаёт сессию
- Поддерживает функцию "запомнить меня"

### Защищённые маршруты

#### Профиль (/profile)
```python
@app.route('/profile')
@login_required
def profile():
    # Отображение профиля пользователя
```
Показывает личную информацию пользователя.

#### Запись на приём (/booking)
```python
@app.route('/booking')
@login_required
def booking():
    # Форма записи на приём
```
Позволяет пользователю выбрать услугу и время приёма.

#### Чат (/chat)
```python
@app.route('/chat')
@login_required
def chat():
    # Чат с администрацией
```
- Отображает историю сообщений
- Позволяет отправлять новые сообщения
- Автоматически отмечает прочитанные сообщения

### Административные маршруты

#### Панель администратора (/admin)
```python
@app.route('/admin')
@admin_required
def admin_dashboard():
    # Административная панель
```
Показывает:
- Статистику
- Последние записи
- Непрочитанные сообщения
- Быстрые действия

#### Управление пользователями (/admin/users)
```python
@app.route('/admin/users')
@admin_required
def admin_users():
    # Управление пользователями
```
Список всех пользователей с возможностью просмотра деталей.

#### Управление записями (/admin/appointments)
```python
@app.route('/admin/appointments')
@admin_required
def admin_appointments():
    # Управление записями
```
Позволяет просматривать и управлять записями на приём.

## Аутентификация и авторизация

### Декораторы
```python
def login_required(f):
    # Проверка авторизации пользователя

def admin_required(f):
    # Проверка прав администратора
```

### Сессии
- Используется Flask-сессии для хранения данных пользователя
- Настроено время жизни сессии (30 дней)
- Поддерживается функция "запомнить меня"

## Система сообщений

### Отправка сообщений
```python
@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_message():
    # Отправка сообщения
```
- Создаёт новое сообщение
- Сохраняет в базе данных
- Возвращает статус отправки

### Чтение сообщений
```python
@app.route('/api/chat/mark-read', methods=['POST'])
def mark_messages_read():
    # Отметка сообщений как прочитанных
```
- Автоматически отмечает сообщения при открытии чата
- Обновляет статус в реальном времени

## Панель администратора

### Статистика
- Общее количество пользователей
- Количество записей на сегодня
- Количество непрочитанных сообщений

### Управление записями
- Просмотр деталей записи
- Изменение статуса
- Добавление заметок

### Медицинские карты
- Создание новых записей
- Просмотр истории болезни
- Управление назначениями

### Чаты с пользователями
- Просмотр всех диалогов
- Быстрый ответ пользователям
- Отметка прочитанных сообщений

## Безопасность

### Защита маршрутов
- Все защищённые маршруты требуют авторизации
- Административные функции доступны только администраторам
- Проверка прав доступа на уровне декораторов

### Обработка данных
- Валидация всех входящих данных
- Безопасное хранение паролей
- Защита от SQL-инъекций через ORM

### Сессии
- Безопасные сессии с секретным ключом
- Настраиваемое время жизни сессии
- Возможность принудительного завершения сессии 