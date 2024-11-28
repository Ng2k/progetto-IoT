#!/bin/bash
ENV=${1:-dev} # di default usa 'dev'

if [ "$ENV" = "prod" ]; then
    docker-compose -f docker-compose.prod.yml up
else
    docker-compose -f docker-compose.dev.yml up
fi