# Use a minimal base image to reduce attack surface
FROM python:3.9-slim

# Python security best practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# SECURITY: Create non-root user and group
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/

# SECURITY: Set file ownership and permissions
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
