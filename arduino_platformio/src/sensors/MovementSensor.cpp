#include "MovementSensor.h"

MovementSensor::MovementSensor(byte pin): _pin(pin) {
    pinMode(pin, INPUT);
};

const byte MovementSensor::getPin() {
    return this->_pin;
}

const Reading MovementSensor::getLastReading() {
	return this->_lastReading;
}

Reading MovementSensor::read() {
	return digitalRead(this->_pin) == HIGH ? Reading::READ : Reading::IDLE;
}

void MovementSensor::updateLastState(Reading lastReading) {
	this->_lastReading = lastReading;
}