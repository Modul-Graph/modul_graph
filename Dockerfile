FROM python:3.12 as builder
RUN pip install poetry
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev ghostscript python3-tk gettext

# Set's up poetry caching and virtualenv configurations
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root
RUN ./gen_translations.sh

FROM python:3.12 as runtime

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --form=builder /app/locales locales


COPY modul_graph ./modul_graph


ENTRYPOINT ["python", "-m", "modul_graph"]
