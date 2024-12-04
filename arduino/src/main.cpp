#include "header.h"
#include "Context.h"

// Functions declaration
bool isTimeForNextReading();

// Global variables
Context* context;

void setup() {;
    context = new Context(
        new IdleState(),
		new MovementSensor(enterSensorPin),
		new MovementSensor(exitSensorPin),
		new LedRgb(ledRgbPins),
        Output::OFF,
		0,
        millis()
    );

    Serial.begin(9600);
}

void loop() {
	if(!isTimeForNextReading()) return;

	context->request();
	context->setLastExecutionTime(millis());
}

// Functions definition:
bool isTimeForNextReading() {
    return millis() - context->getLastExecutionTime() >= frequency;
}