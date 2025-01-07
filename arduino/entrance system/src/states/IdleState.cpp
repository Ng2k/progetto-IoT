#include "State.h"

void IdleState::handle(Context* ctx)
{
	if(millis() - this->_lastTime <= this->_delayDebounce) return;
	ctx->setContextOutput(Output::Off);

	LedRgb* ledRgb = ctx->getLedRgb();
	ledRgb->clearColors();

	MovementSensor* enterSensor = ctx->getEnterSensor();
	MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::Idle);
    exitSensor->updateLastState(Reading::Idle);

	bool isEnterHigh = enterSensor->isHigh();
	bool isExitHigh = exitSensor->isHigh();
	
	if (isEnterHigh || isExitHigh) {
		this->_lastTime = millis();

		//Serial.println("condition: " + String(isExitHigh && ctx->getPeopleCount() <= 0));
		if (isExitHigh && ctx->getPeopleCount() <= 0) {
			ctx->setContextState(new ErrorState());
		}
		else if(isEnterHigh) {
			enterSensor->updateLastState(Reading::Read);
			ctx->setContextState(new WaitingForTransition());
		}
		else if(isExitHigh) {
			exitSensor->updateLastState(Reading::Read);
			ctx->setContextState(new WaitingForTransition());
		}
	}
};