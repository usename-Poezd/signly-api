FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y g++ ffmpeg libsm6 libxext6
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
