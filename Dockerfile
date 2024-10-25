ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 8000
EXPOSE 8080
EXPOSE 5432

CMD fastapi dev /app/src/main.py --host 0.0.0.0 --port 81
