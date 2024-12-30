FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apt update
RUN pip install --upgrade pip \
    && pip install poetry
COPY . /code/
RUN poetry install --without dev
EXPOSE 8000
CMD ["poetry", "run", "unicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "18000", "--bind", "0.0.0.0:8000"]
