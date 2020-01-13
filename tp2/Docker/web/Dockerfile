FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
RUN pip install pipenv
COPY . /code/
RUN pipenv install --dev