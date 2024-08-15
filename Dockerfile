FROM python:3.12 as base

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

CMD ["poetry", "run", "app"]
