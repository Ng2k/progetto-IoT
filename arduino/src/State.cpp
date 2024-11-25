#include <Arduino.h>

#include "State.h"
#include "sensors/InfraRed.h"
#include "../Constants.h"

State::State() {};

void IdleState::handle(Context* ctx)
{
    /* Serial.println("-------------------------------------");
    Serial.println("IDLE"); */
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

	ctx->setContextOutput(Output::OFF);

	InfraRed* enterSensor = ctx->getEnterSensor();
	InfraRed* exitSensor = ctx->getExitSensor();

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

void ReadInIdleState::handle(Context* ctx)
{
    /* Serial.println("-------------------------------------");
    Serial.println("READ_IN_IDLE"); */
    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

    ctx->setContextOutput(Output::OFF);

    InfraRed* enterSensor = ctx->getEnterSensor();
    InfraRed* exitSensor = ctx->getExitSensor();

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

void ReadOutIdleState::handle(Context* ctx)
{
    /* Serial.println("-------------------------------------");
    Serial.println("READ_OUT_IDLE"); */

    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(idleRgb);

    ctx->setContextOutput(Output::OFF);

    InfraRed* enterSensor = ctx->getEnterSensor();
    InfraRed* exitSensor = ctx->getExitSensor();

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

void EnterState::handle(Context* ctx)
{
    /* Serial.println("-------------------------------------");
    Serial.println("ENTER"); */

    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(enterRgb);

    ctx->setContextOutput(Output::ENTER);
    ctx->incrementPeopleCount();

    Serial.println("people: " + String(ctx->getPeopleCount()));

    InfraRed* enterSensor = ctx->getEnterSensor();
    InfraRed* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::READ);
    exitSensor->updateLastState(Reading::READ);

    //todo: chiedere al prof come aggiungere un delay
    ctx->setContextState(new IdleState());
}

void ExitState::handle(Context* ctx)
{
    /* Serial.println("-------------------------------------");
    Serial.println("EXIT"); */

    LedRgb* ledRgb = ctx->getLedRgb();
    ledRgb->changeLedColor(exitRgb);

    ctx->setContextOutput(Output::EXIT);
    ctx->decrementPeopleCount();

    Serial.println("people: " + String(ctx->getPeopleCount()));

    InfraRed* enterSensor = ctx->getEnterSensor();
    InfraRed* exitSensor = ctx->getExitSensor();

    enterSensor->updateLastState(Reading::READ);
    exitSensor->updateLastState(Reading::READ);

    //todo: chiedere al prof come aggiungere un delay
    ctx->setContextState(new IdleState());
}
