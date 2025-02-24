#!/bin/bash

CONFIG=""
TZ="UTC"

# Parse args
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config) CONFIG="$2"; shift ;;
        --tz) TZ="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$CONFIG" ]; then
    echo "Please provide a config file using --config"
    exit 1
fi

# Run
CONFIG=$CONFIG TZ=$TZ docker compose up
CONFIG=$CONFIG docker compose down --remove-orphans
