#include <Arduino.h>

#include "../../Constants.h"
#include "InfraRed.h"

InfraRed::InfraRed(byte pin): _pin(pin) {
    pinMode(pin, INPUT);
};

const byte InfraRed::getPin() {
    return this->_pin;
}

Reading InfraRed::read() {
	this->_lastReading = this->_currentReading;

	if(digitalRead(this->_pin) == HIGH) {
		this->_currentReading = Reading::READ;
		return this->_currentReading;
	}

	this->_currentReading = Reading::IDLE;
	return this->_currentReading;
}