# ================================================================
# STAGE 1 — Build stage
# Install dependencies in a separate layer first
# ================================================================
FROM python:3.11-slim AS builder

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer separately
# So if your code changes but requirements don't, this step is skipped
COPY requirements.txt .

# Install dependencies into a separate folder we can copy later
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ================================================================
# STAGE 2 — Final runtime image
# Lean, clean, only what's needed to RUN the app
# ================================================================
FROM python:3.11-slim AS runner

# Who made this image — good practice for team projects
LABEL maintainer="your-email@example.com"
LABEL project="weather-dashboard"

# Create a non-root user for security
# Running as root inside a container is dangerous
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy your application code
COPY app.py .
COPY requirements.txt .

# Tell Docker this container listens on port 5000
EXPOSE 5000

# Set environment variable defaults
# These are NOT secret values — just configuration
ENV FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Switch to non-root user before running the app
USER appuser

# Health check — Docker uses this to know if your app is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# The command that runs when the container starts
CMD ["python", "app.py"]