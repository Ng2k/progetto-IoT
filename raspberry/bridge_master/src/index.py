import os

from .controllers.main_controller import MainController
from .clients.mqtt_client import MqttClient
from .writer.csv_writer import CsvWriter

def main():
	csv_writer = CsvWriter(
		file="aggregated_data.csv",
		headers=["mc_id", "people", "timestamp"]
	)
	controller = MainController(
		MqttClient(csv_writer),
		csv_writer
	)

	controller.run()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("fine giornata / evento")
		#todo: svuota csv e carica tutto su db