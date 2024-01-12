FROM python:3.11-slim-buster

LABEL org.opencontainers.image.authors="Jesus Legarda"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

RUN prisma generate

RUN prisma db push

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
