#! /bin/bash
set -e 

docker compose --env-file local.env --file test/docker-compose.yaml up -d

docker exec -it nginx /bin/sh -c "ln -s /data/www/node_modules /data/dev/www/node_modules && cd /data/dev/www && npm run dev -- --port 5173 --host"
