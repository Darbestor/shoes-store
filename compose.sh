#!/bin/sh

rm -f .env
for d in */ ; do
    cat $d.env >> .env 2>/dev/null
done
docker compose "$@"
