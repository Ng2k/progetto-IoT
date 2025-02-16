# Utilizza Debian 12 (Bookworm) come immagine base
FROM debian:bookworm

# Mantieni il container aggiornato e installa Python 3
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 \
       python3-pip \
       python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crea una directory di lavoro nel container
WORKDIR /app

# Copia solo i file di dipendenze per installarle e mantenere la cache
COPY requirements.txt /app/requirements.txt

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installa le dipendenze come fase separata
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Copia solo i file dell'applicazione. Questo layer cambierà solo se i file sorgente cambiano.
COPY . /app

# Comando di avvio del container
CMD ["python3", "-m", "src.index"]