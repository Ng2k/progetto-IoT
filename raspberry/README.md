# Raspberry PI - Bridge

## Table of contents
- [Raspberry PI - Bridge](#raspberry-pi---bridge)
	- [Table of contents](#table-of-contents)
	- [Docker](#docker)
		- [setup.sh](#setupsh)
		- [start.sh](#startsh)
	- [Virtual Environment](#virtual-environment)
	- [Authors](#authors)

## Docker

Prima di poter eseguire il programma è necessario impostare l'ambiente virtuale di python e installare le librerie.

### setup.sh

Esegui il file `setup.sh` per installare docker e docker-compose, impostare i permessi all'utente per docker ed eseguire il reboot del sistema per rendere valide le modifiche ai permessi

	$ chmod +x setup.sh
	$ ./setup.sh

### start.sh

Nel caso avessi già docker e docker-compose installato, allora sarà necessario solamente eseguire il file `start.sh`, il programma aggiungerà i permessi per l'accesso alla porta seriale e eseguirà i container

	$ chmod +x start.sh
	$ ./start.sh [--env] [--update-system]

Il flag `--env` serve per specificare che ambiente di sviluppo si vuole avviare. Flag opzionale, valore di default `dev`

Il flag `--update-system` serve per suggerire al programma di aggiornare il sistema operativo. Flag opzionale, nel caso non venisse inserito non si farebbe l'aggiornamento

> ATTENZIONE
>
> Il flag `--env` serve per specificare che ambiente di sviluppo si vuole avviare. Flag opzionale, valore di default `dev`
>
> 	*Esempio*
>
>		$ chmod +x start.sh
>		$ ./start.sh --env dev
>
> Il flag `--update-system` serve per suggerire al programma di aggiornare il sistema operativo. Flag opzionale, nel caso non venisse inserito non si farebbe l'aggiornamento
>
> 	*Esempio*
> 
> 		$ chmod +x start.sh
>		$ ./start.sh --update-system

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

> **ATTENZIONE**
>
> Nel caso si volesse testare il sistema in locale con i virutal environment di python-venv, dovrai installare il broker mqtt sulla macchina e settarlo con queste impostazioni:
>
> 		// file: mqtt.conf
> 		listener 1883
> 		allow_anonymous true
>
> 		$ mosquitto -v -c mqtt.conf

## Authors

- [Nicola Guerra](https://github.com/Ng2k)
- [Tommaso Mortara](https://github.com/Tommyjak)