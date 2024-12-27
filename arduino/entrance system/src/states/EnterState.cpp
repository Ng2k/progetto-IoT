#include "State.h"

void EnterState::handle(Context* ctx)
{
    ctx->setContextOutput(Output::Enter);
    ctx->incrementPeopleCount();

    Serial.println(String(ctx->getPeopleCount()));

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::Read);
    exitSensor->updateLastState(Reading::Read);

    this->_lastTime = millis();
    ctx->setContextState(new IdleState());
}