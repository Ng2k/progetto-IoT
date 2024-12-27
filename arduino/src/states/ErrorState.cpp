#include "State.h"

void ErrorState::handle(Context* ctx) {
	Serial.("Error");
	ctx->setContextOutput(Output::Error);
	this->_lastTime = millis();
	ctx->setContextState(new IdleState());
};