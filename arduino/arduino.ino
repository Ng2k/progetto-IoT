#include "InfraRed.h"
#include "Constants.h"
#include "LedRgb.h"
#include "Context.h"
#include "State.h"

// Contesto del sistema
Context* context;

void setup() {
    context = new Context(
        new IdleState(),
        new InfraRed(enterInfraRedPin),
        new InfraRed(exitInfraRedPin),
        new LedRgb(ledRgbPins),
        Output::OFF,
        0,
        millis()
    );

    Serial.begin(9600);
}

void loop() {
    unsigned long lastExecTime =  context->getLastExecutionTime();
    if(millis() - lastExecTime < frequency) {
        return;
    }

    context->request();
    context->setLastExecutionTime(millis());
}