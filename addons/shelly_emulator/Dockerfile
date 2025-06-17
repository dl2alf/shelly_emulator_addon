ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11-slim

FROM ${BUILD_FROM}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shelly_emulator.py .

EXPOSE 80

CMD ["python3", "shelly_emulator.py"]
