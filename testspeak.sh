docker build -f Dockerfile_speak -t python-speak-app .
docker run --rm -e PYTHONUNBUFFERED=1 -v "$PWD/secret.py:/app/secret.py:ro" python-speak-app


