FROM python:3.13

WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better layer caching
COPY pyproject.toml README.md ./

RUN pip install --no-cache-dir -e .


COPY ./src /code/src

EXPOSE 80

# Command to run the application
CMD ["fastapi", "run", "src/app/main.py", "--host", "0.0.0.0", "--port", "80"]