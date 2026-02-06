FROM python:3.11-slim

# Core environment settings
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

# System dependencies commonly needed for Python projects
# (build tools, git, and basic networking utilities)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
      curl && \
    rm -rf /var/lib/apt/lists/*

# First copy only project metadata to maximize Docker layer caching
COPY pyproject.toml README.md ./

# Install Python dependencies, including test extras
RUN pip install --upgrade pip && \
    pip install .[test]

# Now copy the rest of the repository (specs, rules, tests, skills, etc.)
COPY . .

# Default command: drop into a shell for development.
# Override with `docker run ... pytest` or similar for CI.
CMD ["/bin/bash"]

