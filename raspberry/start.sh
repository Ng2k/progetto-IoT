#!/bin/bash

# Settaggio dell'ambiente (default: 'dev')
ENV=${1:-dev}

# Interrompe lo script in caso di errori
set -e

# Main script
main() {
	if [ "$ENV" = "prod" ]; then
		docker-compose --env-file .env.prod -f docker-compose.prod.yml up --build -d
	else
		docker-compose --env-file .env.dev -f docker-compose.dev.yml up --build -d
	fi
	echo "Container avviati con successo."
}

main