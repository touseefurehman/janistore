# Use official Python image
FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "ecomer.wsgi:application", "--bind", "0.0.0.0:8000"]
