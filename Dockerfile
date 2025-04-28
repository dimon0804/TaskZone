# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем зависимость для работы с PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через Poetry
RUN poetry install --no-interaction --no-dev

# Копируем весь проект в контейнер
COPY . /app/

# Открываем порт для работы
EXPOSE 8000

# Запускаем бота
CMD ["poetry", "run", "python", "main.py"]
