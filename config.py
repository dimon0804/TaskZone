import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEBUG = True

if DEBUG:
    DB_USER = "postgres"
    DB_PASSWORD = "qwerty"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "taskzone"
else:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TASK_STATUSES = {
    "not_started": "Не начато",
    "in_progress": "В процессе",
    "pending_review": "Ожидание проверки",
    "needs_revision": "Требует доработки",
    "completed": "Завершено",
    "canceled": "Отменено",
    "paused": "Приостановлено"
}

TASK_PRIORITIES = {
    "none": "Без приоритета",
    "low": "Низкий",
    "medium": "Средний",
    "high": "Высокий",
    "urgent": "Срочный"
}

LOG_ACTIONS = {
    "task_create": "Создать задачу",
    "task_update": "Обновить задачу",
    "task_delete": "Удалить задачу",
    "task_assign": "Назначить исполнителя задачи",
    "task_unassign": "Снять исполнителя задачи",
    "task_start": "Начать выполнение задачи",
    "task_pause": "Приостановить выполнение задачи",
    "task_complete": "Завершить задачу",
    "task_cancel": "Отменить задачу",
    "task_review": "Отправить задачу на проверку",
    "task_revise": "Запросить доработку задачи",
    "project_create": "Создать проект",
    "project_update": "Обновить проект",
    "project_delete": "Удалить проект",
    "project_assign": "Назначить участника проекта",
    "project_unassign": "Снять участника проекта",
    "user_login": "Вход пользователя",
    "user_logout": "Выход пользователя",
    "user_register": "Регистрация пользователя",
    "user_update": "Обновить данные пользователя"
}

NOTIFICATION_HOUR = 23
NOTIFICATION_MINUTE = 34