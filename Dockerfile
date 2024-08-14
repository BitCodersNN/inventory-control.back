FROM python:3.12 as base

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . /app/

WORKDIR /app

CMD ["poetry", "run", "python", "src/__main__.py"]
