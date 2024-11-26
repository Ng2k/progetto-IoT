#include "Context.h"

Context::Context(
    State* contextState,
    MovementSensor* enterSensor,
    MovementSensor* exitSensor,
    LedRgb* ledRgb,
    Output contextOutput,
    int peopleCount,
    unsigned long lastExecutionTime
)
{
    this->_contextState = contextState;
    this->_enterSensor = enterSensor;
    this->_exitSensor = exitSensor;
    this->_ledRgb = ledRgb;
    this->_contextOutput = contextOutput;
    this->_peopleCount = peopleCount;
    this->_lastExecutionTime = lastExecutionTime;
}

void Context::request() {
    State* ctxState = this->getContextState();
	ctxState->handle(this);

    LedRgb* ledRgb = this->_ledRgb;
	switch (this->getContextOutput())
	{
		case Output::ENTER:
			ledRgb->changeLedColor(enterRgb);
			break;
		case Output::EXIT:
			ledRgb->changeLedColor(exitRgb);
			break;
		default:
			ledRgb->changeLedColor(idleRgb);
			break;
	}
}