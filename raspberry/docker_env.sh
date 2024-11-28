#!/bin/bash
ENV=${1:-dev} # di default usa 'dev'

if [ "$ENV" = "prod" ]; then
    docker-compose -f docker-compose.prod.yml up --build -d
else
    docker-compose -f docker-compose.dev.yml up --build -d
fi