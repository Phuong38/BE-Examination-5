FROM python:3.10-slim-buster
LABEL authors="phuonglt"

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]