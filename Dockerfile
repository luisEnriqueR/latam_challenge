FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

ENV PORT=8080

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]