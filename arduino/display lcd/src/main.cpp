/**
 * @brief Display LCD
 */
#include <Arduino.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

const byte sda = 11;
const byte scl = 12;

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup()
{
	Wire.begin(sda, scl);

	lcd.init();                      // initialize the lcd 
	lcd.backlight();
	lcd.print("Hello, world!");
	Serial.begin(9600);
	Serial.println("Hello, world!");
}

void loop()
{
	if(!Serial.available()) { return; }

	lcd.clear();
	lcd.print(Serial.readStringUntil('\n'));
}