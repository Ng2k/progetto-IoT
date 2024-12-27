#include "State.h"

void WaitingForTransition::handle(Context* ctx) {
	unsigned long currentTime = millis();
	if(currentTime - this->_lastTime <= this->_delayDebounce) return;

	MovementSensor* enterSensor = ctx->getEnterSensor();
	MovementSensor* exitSensor = ctx->getExitSensor();

	bool isEnterHigh = enterSensor->isHigh();
	bool isExitHigh = exitSensor->isHigh();

	Reading enterSensorLastReading = enterSensor->getLastReading();
	bool isMoreEntries = isEnterHigh && enterSensorLastReading == Reading::Read;

	Reading exitSensorLastReading = exitSensor->getLastReading();
	bool isMoreExits = isExitHigh && exitSensorLastReading == Reading::Read;

	if(!isMoreEntries && !isMoreExits && !isEnterHigh && !isExitHigh) return;

	this->_lastTime = currentTime;

	if(isMoreEntries || isMoreExits) ctx->setContextState(new ErrorState());
	else if (isEnterHigh) ctx->setContextState(new ExitState());
	else if (isExitHigh) ctx->setContextState(new EnterState());
}