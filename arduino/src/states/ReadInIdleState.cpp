#include "State.h"

void ReadInIdleState::handle(Context* ctx)
{
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

    ctx->setContextOutput(Output::OFF);

    MovementSensor* enterSensor = ctx->getEnterSensor();
    MovementSensor* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::READ);
    exitSensor->updateLastState(Reading::IDLE);

    if(
        enterSensor->read() == Reading::IDLE &&
        exitSensor->read() == Reading::READ
    ) {
        ctx->setContextState(new EnterState());
    } else if (
        enterSensor->read() == Reading::READ &&
        exitSensor->read() == Reading::IDLE
    ) {
        ctx->setContextState(new IdleState());
    }
}