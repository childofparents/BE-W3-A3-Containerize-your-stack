FROM python:3.10-slim

WORKDIR /app

# Copy dependency requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run uvicorn on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]