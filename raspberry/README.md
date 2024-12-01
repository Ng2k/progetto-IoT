# Raspberry PI - Bridge

## Table of contents
- [Raspberry PI - Bridge](#raspberry-pi---bridge)
	- [Table of contents](#table-of-contents)
	- [Docker](#docker)
		- [setup.sh](#setupsh)
		- [start.sh](#startsh)
		- [docker-compose](#docker-compose)
	- [Virtual Environment](#virtual-environment)
	- [Logs](#logs)
	- [Authors](#authors)

## Docker

Prima di poter eseguire il programma è necessario impostare l'ambiente virtuale di python e installare le librerie.

### setup.sh

Esegui il file `setup.sh` per installare docker e docker-compose, impostare i permessi per far accedere alla porta seriale ed eseguire i container

	$ chmod +x setup.sh
	$ ./setup.sh [default=dev]

> ATTENZIONE
>
> Quando esegui il file bash ricordati di inserire in input anche il tipo di environment desiderato, in questo modo verranno caricate le configurazioni giuste. Il valore di default è "dev"
>
> 	*Esempio*
>
>		$ chmod +x setup.sh
>		$ ./setup.sh dev

### start.sh

Nel caso avessi già docker e docker-compose installato, allora sarà necessario solamente eseguire il file `start.sh`, il programma aggiungerà i permessi per l'accesso alla porta seriale e eseguirà i container

	$ chmod +x start.sh
	$ ./start.sh [default=dev]

> ATTENZIONE
>
> Quando esegui il file bash ricordati di inserire in input anche il tipo di environment desiderato, in questo modo verranno caricate le configurazioni giuste. Il valore di default è "dev"
>
> 	*Esempio*
>
>		$ chmod +x start.sh
>		$ ./start.sh dev

### docker-compose

Per avere un ambiente out-of-the-box è possibile usare `docker` usando `docker compose`.

Eseguire dal terminale il comando per avviare il container con l'ambiente virtuale python già settato e pronto all'utilizzo

	$ export DOCKER_BUILDKIT=1
	$ docker-compose --env-file .env.[dev|prod] -f docker-compose.yml up --no-build -d

Esempio:

	$ export DOCKER_BUILDKIT=1
	$ docker-compose --env-file .env.dev -f docker-compose.yml up --no-build -d

Il comando `export DOCKER_BUILDKIT=1` serve per indicare a docker di usare il build kit e la cache

Il flag `--env-file` serve per passare un file di variabili di ambiente da settare nel container. Il file si deve chiamare `.env.dev` oppure `.env.prod` in base se si tratta di ambiente di sviluppo o produzione

il flag `-f` serve per poter usare un file `docker-compose.yml` custom

Il flag `--no-build` serve per ricostruire evitare il build del container ad ogni utilizzo.

Il flag `-d` serve per far eseguire il container in background

## Virtual Environment

Prima di poter eseguire il programma è necessario che venga creato un ambiente virtuale di python dove poter installare tutte le librerie segnate nel file `requirements.txt` per ogni bridge

	$ cd ./bridge-master
	$ python3 -m venv <nome_a_scelta>_venv
	$ . <nome_ambiente>/bin/activate
	$ pip install --upgrade pip && pip install -r requirements.txt

	$ cd ./bridge-slave
	$ python3 -m venv <nome_a_scelta>_venv
	$ . <nome_ambiente>/bin/activate
	$ pip install --upgrade pip && pip install -r requirements.txt

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