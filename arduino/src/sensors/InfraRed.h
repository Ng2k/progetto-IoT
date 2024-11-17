#ifndef INFRA_RED_H
#define INFRA_RED_H

#include <Arduino.h>

#include "../../Constants.h"

class InfraRed
{
    private:
        const byte _pin;
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
         * @brief Funzione per la lettura dello stato del sensore
         * 
         * @return stato del sensore
         */
        const Reading getLastReading();

        /**
		 * @brief Legge lo stato del sensore di movimento.
		 *
		 * Questa funzione legge lo stato del sensore di movimento,
		 * lo imposta come stato del sensore e lo restituisce.
		 */
		Reading read();

        /**
         * @brief Aggiorna l'ultimo stato del sensore
         * 
         * @param lastReading ultimo stato del sensore
         */
        void updateLastState(Reading lastReading);
};

#endif // INFRA_RED_H