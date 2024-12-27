#include "State.h"

void ExitState::handle(Context* ctx)
{
	LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->setErrorColors();

    ctx->setContextOutput(Output::Exit);
    ctx->decrementPeopleCount();

    Serial.println(String(ctx->getPeopleCount()));

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::Read);
    exitSensor->updateLastState(Reading::Read);

    this->_lastTime = millis();
    ctx->setContextState(new IdleState());
}