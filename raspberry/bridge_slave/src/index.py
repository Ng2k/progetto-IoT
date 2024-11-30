"""
Author:
	- Nicola Guerra <nicola.guerra@outlook.com>
    - Tommaso Mortara <>
"""
import asyncio
import os

from dotenv import load_dotenv

from .log_handler import LogHandler
from .device_scanner import DeviceScanner
from .communications.bridge.mqtt_config import MqttConfig
from .controllers.main_controller import MainController

load_dotenv(
    dotenv_path = (
        "./env.prod" if os.getenv("PYTHON_ENV") == "production" else ".env.dev"
    )
)

def get_mqtt_configs() -> MqttConfig:
    """Get the MQTT configurations
    
    Returns:
        MqttConfig: The MQTT configurations
    """
    return MqttConfig(
        broker=os.getenv("MQTT_BROKER"),
        port=int(os.getenv("MQTT_PORT")),
        keepalive=int(os.getenv("MQTT_KEEPALIVE")),
        sub_topic=os.getenv("MQTT_SUB_TOPIC"),
        pub_topic=os.getenv("MQTT_PUB_TOPIC")
    )

async def main():
    """Start the program"""
    log_handler = LogHandler(os.getenv("LOG_DIR"))
    device_scanner = DeviceScanner(log_handler)
    devices_available = await device_scanner.scan_devices()
    controller = MainController(
        device_list=devices_available,
        mqtt_config=get_mqtt_configs(),
        log_handler=log_handler
    )

    # Run the application
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
