# 1. Use official Python image as base
FROM python:3.10-slim

# 2. Set environment variables for cleaner output and no .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# 6. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 7. Copy the entire Django project
COPY . /app/

# 8. Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# 9. Expose the port for gunicorn
EXPOSE 8000

# 10. Run gunicorn as the default entrypoint
# CMD ["sh", "-c", "python manage.py migrate && python3 manage.py runserver "]
CMD ["sh", "-c", "python manage.py migrate && gunicorn python_lms.wsgi:application --bind 0.0.0.0:8000"]



