docker build -f Dockerfile_mqtt -t python-mqtt-app .
docker run --rm -e PYTHONUNBUFFERED=1 -v "$PWD/secret.py:/app/secret.py:ro" python-mqtt-app


