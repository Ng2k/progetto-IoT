#include "State.h"

void ReadOutIdleState::handle(Context* ctx)
{
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

    ctx->setContextOutput(Output::OFF);

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::IDLE);
    exitSensor->updateLastState(Reading::READ);

    if(
        enterSensor->read() == Reading::READ &&
        exitSensor->read() == Reading::IDLE &&
        ctx->getPeopleCount() > 0
    ) {
        ctx->setContextState(new ExitState());
    } else if (
        enterSensor->read() == Reading::IDLE &&
        exitSensor->read() == Reading::READ
    ) {
        ctx->setContextState(new IdleState());
    }
}