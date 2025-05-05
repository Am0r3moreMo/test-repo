FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create true

WORKDIR /app
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-interaction --no-ansi

COPY . .

# ENV DJANGO_SETTINGS_MODULE=music.settings
# ENV PYTHONUNBUFFERED=1

#RUN poetry run python musicshop/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["poetry", "run", "python", "musicshop/manage.py", "runserver", "0.0.0.0:8000", "--noreload"]