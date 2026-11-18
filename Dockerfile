# Stage 1: Builder
FROM python:3.12-slim AS builder
WORKDIR /app
# Create a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Install build dependencies if needed, then install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Stage 2: Final Runtime
FROM python:3.12-slim
WORKDIR /app
# Copy only the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]