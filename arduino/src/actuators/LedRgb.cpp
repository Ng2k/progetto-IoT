#include "LedRgb.h"

LedRgb::LedRgb(const byte pins[3])
{
    for (int i = 0; i < 3; ++i) {
        this->_pins[i] = pins[i];
        pinMode(this->_pins[i], OUTPUT);
    }
};

byte* LedRgb::getPins() { return this->_pins; };
byte* LedRgb::getRgbValues() { return this->_rgbValues; };

void LedRgb::changeLedColor(const byte rgbValues[3])
{
	for(unsigned char i = 0; i < 3; i++) {
		this->_rgbValues[i] = rgbValues[i];
		analogWrite(this->_pins[i], rgbValues[i]);
	}
}

void LedRgb::setErrorColors() { changeLedColor(errorRgb); }
void LedRgb::setExitColors() { changeLedColor(exitRgb); }
void LedRgb::setEnterColors() { changeLedColor(enterRgb); }
void LedRgb::clearColors() { changeLedColor(clearRgb); }