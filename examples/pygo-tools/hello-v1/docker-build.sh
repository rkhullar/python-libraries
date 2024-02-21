tar --exclude='local' --exclude='venv' -cvh ./* | docker build -t pygo-hello-build -
docker compose up
