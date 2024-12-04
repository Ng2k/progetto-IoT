#include "State.h"

void ExitState::handle(Context* ctx)
{
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(exitRgb);

    ctx->setContextOutput(Output::EXIT);
    ctx->decrementPeopleCount();

    Serial.println("people: " + String(ctx->getPeopleCount()));

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::READ);
    exitSensor->updateLastState(Reading::READ);

    ctx->setContextState(new IdleState());
}