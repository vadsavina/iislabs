FROM python:3.11-slim

COPY . /ml_service
VOLUME /models
WORKDIR /ml_service

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Podman:
# podman build . --tag mobile_classifier_model:1
# podman run -p 8000:8000 -v $(pwd)/../models:/models:z mobile_classifier_model:1

# Docker (альтернатива):
# docker build . --tag mobile_classifier_model:1
# docker run -p 8000:8000 -v $(pwd)/../models:/models mobile_classifier_model:1