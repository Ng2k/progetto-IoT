import json
import csv
from pathlib import Path

import paho.mqtt.client as mqtt

# Configurazione
BROKER = "localhost"  # Es. "192.168.1.100"
PORT = 1883
TOPIC = "bridge/+/microcontroller/+/people"  # "+" è un wildcard per ascoltare tutti i bridge e microcontrollori
CSV_FILE = Path("aggregated_data.csv")

def write_to_csv(mc_id, people, timestamp):
    """Scrive i dati nel file CSV."""
    write_header = not CSV_FILE.exists()  # Aggiungi header se il file non esiste
    with open(CSV_FILE, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["device_serial_number", "people", "timestamp"])
        writer.writerow([mc_id, people, timestamp])

# Callback per la ricezione dei messaggi
def on_message(client, userdata, msg):
	print(f"Messaggio ricevuto: {msg.topic}")
	try:
		payload = json.loads(msg.payload.decode('utf-8'))
		print(json.dumps(payload, indent=4))

		mc_id = payload["device_serial_number"]
		people = payload["people"]
		timestamp = payload["timestamp"]
		
		# Scrittura nel file CSV
		write_to_csv(mc_id, people, timestamp)
	except Exception as e:
		print(f"Errore nella gestione del messaggio: {e}")

def main():
	# Configurazione del client MQTT
	client = mqtt.Client()
	client.on_message = on_message
	client.connect(BROKER, PORT, 60)
	
	# Iscrizione al topic per ricevere i dati
	client.subscribe(TOPIC)
	print(f"In ascolto sul topic {TOPIC}...")
	
	client.loop_forever()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("fine giornata / evento")
		#todo: svuota csv e carica tutto su db