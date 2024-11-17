#include <ArduinoBLE.h>

const char* deviceName = "Nano33IoT";

// BLE service and characteristic
BLEService myService("180A"); // Custom service UUID
BLEStringCharacteristic myCharacteristic("2A56", BLERead | BLEWrite, 20); // Read/Write, max 20 characters

void setup() {
    Serial.begin(9600);
    while (!Serial);

    if (!BLE.begin()) {
        Serial.println("Starting BLE failed!");
        while (1);
    }

    // Add service and characteristic
    BLE.setDeviceName(deviceName);
    BLE.setLocalName(deviceName);
    BLE.setAdvertisedService(myService);
    myService.addCharacteristic(myCharacteristic);
    BLE.addService(myService);

    BLE.advertise();
    Serial.println("BLE advertising with service...");
}

void loop() {
    BLEDevice central = BLE.central(); // Check for connections

    if (central) {
        Serial.println("Connected to central device!");

        while (central.connected()) {
            // Send "test data" periodically
            myCharacteristic.setValue("test data");
            delay(1000); // Adjust interval as needed
        }

        Serial.println("Disconnected from central device");
    }
}