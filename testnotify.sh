docker build -f Dockerfile_notify -t python-httpx-notify-app .
docker run --rm -v "$PWD/secret.py:/app/secret.py:ro" python-httpx-notify-app



