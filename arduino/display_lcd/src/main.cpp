#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);

const byte sda = 11;
const byte scl = 12;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(sda, scl);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.println("ciao");
}

void loop() {
  // put your main code here, to run repeatedly:
}