#include "State.h"

void ErrorState::handle(Context* ctx) {
	Serial.println("Error");
	ctx->setContextOutput(Output::Error);
	this->_lastTime = millis();
	ctx->setContextState(new IdleState());
};