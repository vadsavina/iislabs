FROM python:3.11-slim

COPY . /requests
WORKDIR /requests

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "send_requests.py"]

# Podman:
# podman build . --tag mobile_requests:1
# podman run --network=host mobile_requests:1
#
# Для работы в compose используется имя сервиса ml_service

