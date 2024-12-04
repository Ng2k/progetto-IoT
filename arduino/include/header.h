#ifndef HEADER_H
#define HEADER_H

#include <Arduino.h> 

// Pin del LED RGB
const byte ledRgbPins[3] = { 11, 9, 7 };

// Pin dei pulsanti
const byte enterSensorPin = 2;
const byte exitSensorPin = 4;

// Colori RGB per diversi stati
const byte idleRgb[3] = { 0, 0, 255 };
const byte exitRgb[3] = { 255, 0, 0 };
const byte enterRgb[3] = { 0, 255, 0 };

// Frequenza di campionamento in millisecondi
const unsigned int frequency = 1000;

// Stati del sensore.
enum class Reading { READ, IDLE };

/**
 * @enum Output
 * @brief Stati di output per controllare l'attuatore (LED RGB).
 */
enum class Output { OFF, ENTER, EXIT };
#endif //HEADER_H