# Raspberry PI - Bridge

## Table of contents
- [Raspberry PI - Bridge](#raspberry-pi---bridge)
	- [Table of contents](#table-of-contents)
	- [Setup](#setup)
		- [Docker](#docker)
		- [Virtual Environment](#virtual-environment)
	- [Authors](#authors)

## Setup

Prima di poter eseguire il programma è necessario impostare l'ambiente virtuale di python e installare le librerie.

### Docker

Per avere un ambiente out-of-the-box è possibile usare `docker` usando `docker compose`.

> **NOTA BENE**
> 
> Prima di avviare il container, devi creare l'immagine utilizzando il Dockerfile. Puoi farlo con il comando docker build
> 	
> 		$ docker build -t raspberry-bridge ./Dockerfile

Eseguire dal terminale il comando per avviare il container con l'ambiente virtuale python già settato e pronto all'utilizzo

	$ docker-compose up


### Virtual Environment

Prima di poter eseguire il programma è necessario che venga creato un ambiente virtuale di python dove poter installare tutte le librerie segnate nel file `requirements.txt`

	$ python3 -m venv <nome_a_scelta>_venv

> **NOTA BENE**
>
> Per convenzione nominare l'ambiente virtuale con il suffisso "_venv" per farlo riconoscere automaticante dal .gitignore

Una volta creato l'ambiente verrà creata una cartella con lo stesso nome dell'ambiente

> **ATTENZIONE**
>
> Non modificare e/o eliminare file da questa cartella, potrebbe causare errori di esecuzione del programma


Prima di proseguire è necessario attivare l'ambiente di sviluppo

	$ . <nome_ambiente>/bin/activate

Una volta attivato l'ambiente basterà solamente aggiornare pip (per evenienza) e proseguire con l'installazione di tutte le librerie necessarie

	$ pip3 install --upgrade pip3 && pip3 install -r requirements.txt

## Authors

- [Nicola Guerra](https://github.com/Ng2k)
- [Tommaso Mortara](https://github.com/Tommyjak)