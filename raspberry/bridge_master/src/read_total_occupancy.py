import requests
import os

from utils import Utils

def get_event_id() -> str:
	# chiamata per ottenere l'evento corrente associato al bridge
	# http://localhost:3000/events/get-current-event?bridge_id=1234
	# { list_stand, id, metadata }
	endpoint = f"{os.getenv('API_URL')}/database/events/get-current-event"
	mp_master_id = Utils.get_serial()
	query_string = f"mp-master-id={mp_master_id}"
	response = requests.get(f"{endpoint}?{query_string}")

	if response.status_code == 200 or response.status_code == 201:
		print("Request inviata con successo")
		print("Risposta API:", response.json())
		return response.json()["data"]["id"]

	print(f"Errore durante l'invio. Status code: {response.status_code}")
	print("Dettagli:", response.text)
	return ""

def main(event_id: str):
	
	# Invio dati all'API
	api_url = os.getenv('API_URL')
	endpoint = f"{api_url}/database/events/{event_id}/get-stands-occupancy"
	response = requests.get(endpoint)

	if response.status_code == 200 or response.status_code == 201:
		print("Riga inviata con successo:")
		print("Risposta API:", response.json())
	else:
		print(f"Errore durante l'invio. Status code: {response.status_code}")
		print("Dettagli:", response.text)

if __name__ == "__main__":
	event_id = get_event_id()
	main(event_id)
	