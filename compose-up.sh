#!/bin/sh

rm .env
for d in */ ; do
    cat $d.env >> .env 2>/dev/null
done
COMPOSE_FILES=$(find . -name \*.yml -printf " -f %p")
docker compose $COMPOSE_FILES up -d
