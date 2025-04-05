docker build -f Dockerfile_vm -t python-httpx-vmonkey-app .
docker run --rm -v "$PWD/secret.py:/app/secret.py:ro" python-httpx-vmonkey-app

