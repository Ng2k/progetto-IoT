#include "State.h"

void IdleState::handle(Context* ctx)
{
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

	ctx->setContextOutput(Output::OFF);

	MovementSensor* enterSensor = ctx->getEnterSensor();
	MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::IDLE);
    exitSensor->updateLastState(Reading::IDLE);

	if(
		enterSensor->read() == Reading::READ &&
		exitSensor->read() == Reading::IDLE &&
        exitSensor->getLastReading() == Reading::IDLE
	) {
		ctx->setContextState(new ReadInIdleState());
	}
	else if(
		enterSensor->read() == Reading::IDLE &&
		exitSensor->read() == Reading::READ &&
        exitSensor->getLastReading() == Reading::IDLE &&
		ctx->getPeopleCount() > 0
	) {
		ctx->setContextState(new ReadOutIdleState());
	}
};