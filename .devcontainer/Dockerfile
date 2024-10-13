FROM python:3.12
RUN pip install poetry
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev ghostscript python3-tk


# Set's up poetry irtualenv configurations
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY . .
