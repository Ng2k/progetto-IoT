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

Eseguire dal terminale il comando per avviare il container con l'ambiente virtuale python già settato e pronto all'utilizzo

	$ docker-compose --env-file .env.<environment> -f docker-compose.dev.yml up --build -d

Il flag `--env-file` serve per passare un file di variabili di ambiente da settare nel container. Il file si deve chiamare `.env.dev` oppure `.env.prod` in base se si tratta di ambiente di sviluppo o produzione

Il flag `--build` serve per ricostruire l'immagine nel caso il file `docker-compose.yml` avesse ricevuto modifiche.

Il flag `-d` serve per far eseguire il container in background

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

	$ pip install --upgrade pip && pip install -r requirements.txt

## Authors

- [Nicola Guerra](https://github.com/Ng2k)
- [Tommaso Mortara](https://github.com/Tommyjak)