FROM python:3.12-slim

# Установка системных зависимостей, включая netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . .

COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh


CMD ["/wait_for_db.sh", "sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py csu && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]

EXPOSE 8000
