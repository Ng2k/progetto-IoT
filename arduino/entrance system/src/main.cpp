#include "header.h"
#include "Context.h"

/* Definizione pin */
const byte enterSensorPin = 2;
const byte exitSensorPin = 4;
const byte ledRgbPins[3] = { 11, 9, 7 };

// Global variables
Context* context;

void setup() {;
    context = new Context(
        new IdleState(),
		new MovementSensor(enterSensorPin),
		new MovementSensor(exitSensorPin),
		new LedRgb(ledRgbPins)
    );

    Serial.begin(9600);
}

void loop() {
	context->request();
}