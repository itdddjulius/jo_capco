FROM python:3.11.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .

ENV TOKENIZERS_PARALLELISM=false

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]