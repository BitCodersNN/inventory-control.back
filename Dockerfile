FROM python:3.12 as base

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-dev

COPY . .

CMD ["poetry", "run", "app"]
