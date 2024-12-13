FROM python:3.12-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev
COPY . .
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py csu && python manage.py runserver 0.0.0.0:8000"]
EXPOSE 8000