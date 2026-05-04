FROM python:3.11-slim

LABEL maintainer="Valentine Golden Ghanem <valentineghanem@gmail.com>"
LABEL description="Vitamin D Ghana Review — Reproducible Analysis Environment"

# System dependencies for geopandas
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libspatialindex-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create output directories
RUN mkdir -p figures data

# Default: run full pipeline
CMD ["python", "scripts/analysis_pipeline.py", "--all"]

# To run Dash app:
# docker run -p 8050:8050 vitd-ghana python app.py
EXPOSE 8050
