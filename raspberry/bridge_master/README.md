# Bridge master

Questo è il codice per tutti i bridge di tipo "slave" del sistema finale.

> **ATTENZIONE**
>
> *Versione Python* -> `3.11.x`
>
> *Sistema Operativo* -> `Raspberry PI OS 64bit (Debian v12, bookworm)`.


## Table of contents
- [Bridge master](#bridge-master)
	- [Table of contents](#table-of-contents)
	- [Setup](#setup)
	- [Test](#test)
	- [Logs](#logs)
	- [Authors](#authors)

## Setup

Prima di avviare il programma bisogna creare un ambiente virtuale per installare tutte le librerie necessarie al progetto

	$ python3 -m venv <nome ambiente>_venv

> **NOTA BENE**
>
> Per convenzione nominare l'ambiente virtuale con il suffisso "_venv" per farlo riconoscere automaticante dal .gitignore

Una volta creato l'ambiente verrà creata una cartella con lo stesso nome dell'ambiente

> **ATTENZIONE**
>
> Non modificare e/o eliminare file da questa cartella, potrebbe causare errori di esecuzione del programma


Prima di proseguire è necessario attivare l'ambiente di sviluppo

	$ . <nome ambiente>/bin/activate

Una volta attivato l'ambiente basterà solamente aggiornare pip (per evenienza) e proseguire con l'installazione di tutte le librerie necessarie

	$ pip install --upgrade pip && pip install -r requirements.txt

## Test

Il progetto usa la libreria [pytest](https://docs.pytest.org/en/stable/getting-started.html) per tutti gli unit test, e [coverage](https://coverage.readthedocs.io/en/6.5.0/) per la creazione di report riguardo la completezza di questi ultimi

Tutti i test vanno salvati dentro la cartella `tests/` e con il nome che rispetti la convenzione `test_*.py`

## Logs

La struttura file dei log di sistema è organizzata nel seguente modo

	logs/
	├── app/
	│   ├── 2024-11-29.log
	│   ├── 2024-11-30.log
	|
	├── errors/
	│   ├── critical/
	│   │   ├── 2024-11-29.log
	│   │   ├── 2024-11-30.log
	│   ├── warnings/
	│   │   ├── 2024-11-29.log
	|
	├── performance/
	│   ├── 2024-11-29.log
	|
	├── security/
	│   ├── auth/
	│   │   ├── 2024-11-29.log
	│   ├── firewall.log
	|
	├── metrics/
	│   ├── cpu_usage.csv
	│   ├── memory_usage.csv
	|
	├── backups/
	│   ├── 2024-10-logs.tar.gz
	│   ├── 2024-11-logs.tar.gz

I log sono raccolti temporalmente e sono divisi in queste categorie:
- In `app/` troviamo i log generati automaticamente dell'applicazione

- In `errors/` troviamo i log generati da errori nel codice, suddivisi in categoria in base alla loro gravità: `critical`, `warnings`

- In `performance` troviamo i log con le prestazioni del programma, tipo tempi di esecuzione dei processi e funzioni

- In `security` troviamo i log rigurdanti autenticazioni, autorizzazioni e firewall

- In `metrics` troviamo i log con le prestazioni della macchina/computer: cpu usage, memory usage ecc...

- In `backups` troviamo i log compressi e pronti ad essere archiviati

## Authors

- [Nicola Guerra](https://github.com/Ng2k)
- [Tommaso Mortara](https://github.com/Tommyjak)