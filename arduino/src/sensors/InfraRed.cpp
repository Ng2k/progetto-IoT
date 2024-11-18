#include <Arduino.h>

#include "../../Constants.h"
#include "InfraRed.h"

InfraRed::InfraRed(byte pin): _pin(pin) {
    pinMode(pin, INPUT);
};

const byte InfraRed::getPin() {
    return this->_pin;
}

const Reading InfraRed::getLastReading() {
	return this->_lastReading;
}

Reading InfraRed::read() {
	return digitalRead(this->_pin) == HIGH ? Reading::READ : Reading::IDLE;
}

void InfraRed::updateLastState(Reading lastReading) {
	this->_lastReading = lastReading;
}