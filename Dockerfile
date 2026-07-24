# Dockerfile for FastMCP Knowledge Tree Server
FROM python:3.11-slim

# Install system tools and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency definition and README.md
COPY pyproject.toml README.md ./

# Install dependencies using uv
RUN uv pip install --system -e .

# Copy project files
COPY . .

# Environment variables for FastMCP HTTP transport
ENV FASTMCP_TRANSPORT=http
ENV FASTMCP_HOST=0.0.0.0
ENV FASTMCP_PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "mcp/server.py"]
