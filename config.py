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
