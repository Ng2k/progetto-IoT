import os

from .controllers.main_controller import MainController
from .clients.mqtt.mqtt_client import MqttClient
from .writer.csv_writer import CsvWriter
from .log_handler import LogHandler
from .clients.mqtt.mqtt_config import MqttConfig

from dotenv import load_dotenv
load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

def main():
	csv_writer = CsvWriter(
		file="aggregated_data.csv",
		headers=["mc_id", "people", "timestamp"],
		log_handler=LogHandler()
	)

	mqtt_config: MqttConfig = MqttConfig(
		broker=os.getenv("MQTT_BROKER"),
		port=int(os.getenv("MQTT_PORT")),
		keepalive=int(os.getenv("MQTT_KEEPALIVE")),
		sub_topic=os.getenv("MQTT_SUB_TOPIC"),
		pub_topic=os.getenv("MQTT_PUB_TOPIC")
	)

	mqtt_client = MqttClient(
		config=mqtt_config,
		writer=csv_writer,
		log_handler=LogHandler()
	)

	controller = MainController(
		client=mqtt_client,
		writer=csv_writer,
		log_handler=LogHandler()
	)

	controller.run()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("fine giornata / evento")
		#todo: svuota csv e carica tutto su db