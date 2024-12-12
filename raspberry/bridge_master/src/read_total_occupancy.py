import requests
import os

from utils import Utils

def setup():
	# chiamata per ottenere l'evento corrente associato al bridge
	# http://localhost:3000/events/get-current-event?bridge_id=1234
	# { list_stand, id, metadata }
	endpoint = f"{os.getenv('API_URL')}/database/events/get-current-event"
	mp_master_id = Utils.get_serial()
	query_string = f"mp-master-id={mp_master_id}"
	print(f"{endpoint}?{query_string}")

	#response = requests.get(f"{endpoint}?{query_string}")


	#if response.status_code == 200 or response.status_code == 201:
	#	print("Request inviata con successo")
	#	print("Risposta API:", response.json())
	#else:
	#	print(f"Errore durante l'invio. Status code: {response.status_code}")
	#	print("Dettagli:", response.text)

def main():
	
	# lettura occupazione stand tramite id evento preso prima
	print("Api url:", f"{os.getenv('API_URL')}/events/{}HYkierUyvjNJQuzl1klz/get-stands-occupancy")

	# Invio dati all'API
	response = requests.post(
		f"{os.getenv('API_URL')}/database/upload-readings",
		json={
			"readings": [ payload ]
		}
	)

	if response.status_code == 200 or response.status_code == 201:
		print("Riga inviata con successo:", row_dict)
		print("Risposta API:", response.json())
	else:
		print(f"Errore durante l'invio. Status code: {response.status_code}")
		print("Dettagli:", response.text)

if __name__ == "__main__":
	setup()
	#main()
	