#ifndef LED_RGB_H
#define LED_RGB_H

#include "header.h"

// Colori RGB per diversi stati
const byte errorRgb[3] = { 255, 0, 0 };
const byte exitRgb[3] = { 0, 0, 255 };
const byte enterRgb[3] = { 0, 255, 0 };
const byte clearRgb[3] = { 0, 0, 0 };

class LedRgb
{
private:
    byte _pins[3];
    byte _rgbValues[3];

    /** @brief Cambia il colore del LED RGB. */
    void changeLedColor(const byte rgbValues[3]);
public:
    /** @brief Costruttore classe LedRGB */
    LedRgb(const byte pins[3]);

    /**
    * @brief Restituisce il pin a cui è collegato il LED RGB.
    * @return Pin a cui è collegato il LED RGB.
    */
    unsigned char* getPins();

    /**
    * @brief Restituisce i valori RGB del LED RGB.
    * @return Valori RGB del LED RGB.
    */
    unsigned char* getRgbValues();

    /** @brief Imposta i colori del LED RGB in caso di errore. */
    void setErrorColors();

    /** @brief Imposta i colori del LED RGB in caso di uscita. */
    void setExitColors();

    /** @brief Imposta i colori del LED RGB in caso di entrata. */
    void setEnterColors();

    /** @brief Spegne il LED RGB. */
    void clearColors();
};

#endif // LED_H