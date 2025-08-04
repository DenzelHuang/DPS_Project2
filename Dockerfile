# Use an official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY benchmark.py /app/

# (Optional) Copy data.csv into image for convenience
COPY data.csv /app/data.csv

# Install dependencies
RUN pip install --no-cache-dir pandas

# Create results directory
RUN mkdir /app/output

# Default environment variables
ENV DATA_FILE=data.csv
ENV OUTPUT_DIR=output

# Run benchmark on container start
CMD ["python", "benchmark.py"]