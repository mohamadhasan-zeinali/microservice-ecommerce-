
FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/


RUN python manage.py migrate
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
