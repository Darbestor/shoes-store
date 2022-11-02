FROM python:3.10-alpine as base

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


FROM base as builder

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM base as final
EXPOSE 8000/tcp
WORKDIR /opt/app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .

ENTRYPOINT ["python3", "consumer.py"]