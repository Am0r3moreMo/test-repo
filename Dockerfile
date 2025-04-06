# Базовый образ
FROM python:3.11-slim-bookworm

# Устанавливаем только необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry (без интеграции с системным Python)
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create true

# Создаем и настраиваем рабочую директорию
WORKDIR /app
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

# Копируем только файлы зависимостей (для кэширования)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта в виртуальное окружение
RUN poetry install --only main --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . .

# # Настройки Django
# ENV DJANGO_SETTINGS_MODULE=music.settings
# ENV PYTHONUNBUFFERED=1

# Собираем статику
#RUN poetry run python musicshop/manage.py collectstatic --noinput

# Порт приложения
EXPOSE 8000

# Команда запуска через виртуальное окружение
CMD ["poetry", "run", "python", "musicshop/manage.py", "runserver", "0.0.0.0:8000", "--noreload"]