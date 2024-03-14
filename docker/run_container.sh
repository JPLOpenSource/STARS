#!/bin/bash

NAME="qm-dev-$USER"
IMG="qm"
WORK_DIR=$(pwd)
TARGET_DIR="/work"

if [[ ! -z $(docker container ls -q --filter "name=$NAME") ]]; then
   echo "Docker is running - attaching"
   # container is running, attach to it
    exec docker exec -it "$NAME" bash
else
    echo "Docker not running - starting and then attaching"
    exec docker run --rm --net host -v \
    "$WORK_DIR":/$NAME --user $(id -u):$(id -g) \
    --name "$NAME" -e USER=$USER \
    -e GIT_COMMITTER_NAME=$USER -e GIT_COMMITTER_EMAIL=${USER}@jpl.nasa.gov \
    -e DISPLAY=host.docker.internal:0 \
    --workdir /$NAME -it $IMG 
fi
