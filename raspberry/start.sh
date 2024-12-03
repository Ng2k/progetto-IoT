#!/bin/bash

main() {
	# Inizializza il progetto
	sudo python3 -m setup.python.start "$@"
}

main "$@"
