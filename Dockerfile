# Multi-stage build for Railway deployment

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
# Install packages while ignoring sqlparse conflicts
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir djongo==1.3.6 --no-deps && \
    pip install --no-cache-dir pymongo==3.12.3 && \
    pip install --no-cache-dir Django==4.2.8 djangorestframework==3.14.0 django-cors-headers==4.3.1 && \
    pip install --no-cache-dir openai==1.54.0 python-dotenv==1.0.0 dnspython==2.4.2 && \
    pip install --no-cache-dir gunicorn==21.2.0 whitenoise==6.6.0 && \
    pip install --no-cache-dir 'sqlparse>=0.3.1'

# Copy backend code
COPY backend/ ./

# Copy startup script
COPY start.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static/frontend

# Copy index.html to templates directory for Django to serve
RUN mkdir -p templates && cp ./static/frontend/index.html ./templates/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (Railway will set PORT environment variable)
EXPOSE 8000

# Start command using Python script to handle PORT variable
CMD ["python", "start.py"]
