#!/bin/sh

rm -f .env
for d in */ ; do
    cat $d.env >> .env 2>/dev/null
    if [ $1 = "up" ]
    then
        ./${d}pre_build_tasks.sh
    fi

done
docker compose "$@"
