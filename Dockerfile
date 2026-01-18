# syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/python:latest-dev AS dev

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin":$PATH
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY src/ src/
COPY --from=dev /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

ENTRYPOINT ["python", "src/web.py"]
