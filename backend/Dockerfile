FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv
RUN uv pip install --no-cache-dir -r <(uv pip compile pyproject.toml)

COPY . /app

EXPOSE 5001
CMD ["uv", "run", "python", "run.py"]
