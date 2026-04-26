FROM python:3.11-slim

WORKDIR /app

# dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy whole project (not just app folder separately)
COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]