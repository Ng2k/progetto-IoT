#ifndef INFRA_RED_H
#define INFRA_RED_H

#include <Arduino.h>

#include "../../Constants.h"

class InfraRed
{
    private:
        const byte _pin;
        Reading _currentReading;
		Reading _lastReading;

    public:
        /**
        * @brief Costruttore classe del sensore a raggi infrarossi
        * 
        * @param pin numero pin dove il sensore è stato inserito
        */
        InfraRed(byte pin);

        /**
        * @brief Funzione per lettura del pin del sensore
        *
        * @return pin del sensore
        */
        const byte getPin();

        /**
		 * @brief Legge lo stato del sensore di movimento.
		 *
		 * Questa funzione legge lo stato del sensore di movimento,
		 * lo imposta come stato del sensore e lo restituisce.
		 */
		Reading read();
};

#endif // INFRA_RED_H