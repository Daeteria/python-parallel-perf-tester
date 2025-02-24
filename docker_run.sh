#!/bin/bash

CONFIG=""
NO_BUILD=false
IMG_NAME="pppt"
TZ="UTC"

# Parse args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config) CONFIG="$2"; shift ;;
        --no-build) NO_BUILD=true ;;
        --img-name) IMG_NAME="$2"; shift ;;
        --tz) TZ="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Build
if [ "$NO_BUILD" = false ]; then
    echo "Building image $IMG_NAME..."
    docker build -t $IMG_NAME -f Dockerfile .
fi

if [ -z "$CONFIG" ]; then
    echo "Please provide a config file using --config"
    exit 1
fi

# Run
docker run --rm -e TZ=$TZ -v ./:/app $IMG_NAME python3 /app/main.py --config=$CONFIG
