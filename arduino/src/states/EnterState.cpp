#include "State.h"

void EnterState::handle(Context* ctx)
{
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(enterRgb);

    ctx->setContextOutput(Output::ENTER);
    ctx->incrementPeopleCount();

    Serial.println(String(ctx->getPeopleCount()));

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::READ);
    exitSensor->updateLastState(Reading::READ);

    ctx->setContextState(new IdleState());
}