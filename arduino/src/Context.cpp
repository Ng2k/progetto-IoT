#include "Context.h"

Context::Context(
    State* contextState,
    MovementSensor* enterSensor, MovementSensor* exitSensor,
    LedRgb* ledRgb
)
    : _peopleCount(0), _contextOutput(Output::Off), _contextState(contextState),
    _enterSensor(enterSensor), _exitSensor(exitSensor), _ledRgb(ledRgb) {}

void Context::request() {
    State* ctxState = this->getContextState();
	ctxState->handle(this);

    LedRgb* ledRgb = this->_ledRgb;
	switch (this->getContextOutput())
	{
		case Output::Enter:
			ledRgb->setEnterColors();
			break;
		case Output::Exit:
			ledRgb->setExitColors();
			break;
        case Output::Error:
            ledRgb->setErrorColors();
            break;
        default:
            break;
	}
}