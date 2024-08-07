FROM python:3.12 as base

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

WORKDIR /app
RUN poetry install --no-root

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

WORKDIR /app

CMD ["poetry", "run", "python", "src/__main__.py"]
