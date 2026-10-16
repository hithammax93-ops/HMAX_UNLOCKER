FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Cache dependencies separately from application and poster changes.
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy only runtime code and assets; credentials are supplied at runtime.
COPY main.py hmax_*.py ./
COPY images/ ./images/

# main.py binds to 0.0.0.0 and reads Railway's injected PORT value.
ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]
