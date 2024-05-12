FROM  python:latest
ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.0 \
  PYTHONPATH=/app

WORKDIR /app


COPY requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir -r /api/requirements.txt

COPY . /app/

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0","--port", "5000"]