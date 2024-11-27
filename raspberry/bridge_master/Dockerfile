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

# Imposta Python 3 come predefinito per il comando "python"
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Crea una directory di lavoro nel container
WORKDIR /app

# Copia eventuali file necessari nella directory di lavoro
COPY . /app

# Step 4: Create a virtual environment inside the container
RUN python -m venv raspberry_IoT_venv

# Step 5: Activate the virtual environment and install dependencies
RUN . raspberry_IoT_venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

# Step 7: Set the environment variable for the virtual environment activation (to make it active in subsequent commands)
ENV VIRTUAL_ENV=/app/raspberry_IoT_venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
