#ifndef LED_RGB_H
#define LED_RGB_H

#include "Constants.h"

class LedRgb
{
    private:
        byte _pins[3];
        byte _rgbValues[3];

    public:
        /** 
        * @brief Costruttore classe LedRGB
        */
        LedRgb(const byte pins[3]);

        /**
        * @brief Restituisce il pin a cui è collegato il LED RGB.
        *
        * @return Pin a cui è collegato il LED RGB.
        */
        unsigned char* getPins();

        /**
        * @brief Restituisce i valori RGB del LED RGB.
        *
        * @return Valori RGB del LED RGB.
        */
        unsigned char* getRgbValues();

        /**
        * @brief Cambia il colore del LED RGB.
        */
        void changeLedColor(const unsigned char rgbValues[3]);
};

#endif // LED_H