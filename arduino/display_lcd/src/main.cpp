#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);

bool i2CAddrTest(uint8_t addr);

void setup() {
	Wire.begin(SDA, SCL); // attach the IIC pin
	if (!i2CAddrTest(0x27)) {
		lcd = LiquidCrystal_I2C(0x3F, 16, 2);
	}
	lcd.init(); 
	lcd.backlight();
	lcd.clear();
	lcd.setCursor(0,0);

	Serial.begin(9600);
}

void loop() {
	if (!Serial.available()) return;

	lcd.clear();
	String complete_data = Serial.readStringUntil('\0');

	int row = 0;  // Inizializziamo dalla riga 0
	int col = 0;  // Inizializziamo dalla colonna 0

	for (unsigned int i=0; i < complete_data.length(); i++){
		char current_char = complete_data[i];

		if(current_char == '\n'){
			row = (row == 1) ? 0 : row + 1 ;

			col = 0;

			lcd.setCursor(col, row);
		} else {
			lcd.print(current_char);
			col++;

			if(col > 15){
				col = 0;
				row = (row == 1) ? 0 : row + 1 ;

				lcd.setCursor(col, row);
			}
		}
	}
}

bool i2CAddrTest(uint8_t addr) {
	Wire.begin();
	Wire.beginTransmission(addr);
	if (Wire.endTransmission() == 0) {
		return true;
	}
	return false;
}