#!/bin/sh

build=false

# if --build flag passed to compose then we should
# execute prebuild tasks for services
for var in "$@"
    do
        if [ "$var" = "--build" ]
        then
            build=true
            break
        fi
done

rm -f .env

for d in */ ; do
    # gather config for all services
    cat $d.env >> .env 2>/dev/null
    
    if [ "$build" = true ] ; then
        echo "Executing pre_build_tasks in directory $d"
        ./${d}pre_build_tasks.sh
    fi
done

docker compose "$@"
