#!/bin/sh

rm -f .env
for d in */ ; do
    cat $d.env >> .env 2>/dev/null
    ./${d}pre_build_tasks.sh
done
docker compose "$@"
