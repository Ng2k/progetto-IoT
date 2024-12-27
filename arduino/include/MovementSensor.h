#ifndef MOVEMENT_SENSOR_H
#define MOVEMENT_SENSOR_H

#include "header.h"

class MovementSensor
{
private:
    const byte _pin;
    Reading _lastReading;

public:
    /**
    * @brief Costruttore classe del sensore a raggi infrarossi
    * @param pin numero pin dove il sensore è stato inserito
    */
    MovementSensor(byte pin);

    /**
    * @brief Funzione per lettura del pin del sensore
    * @return pin del sensore
    */
    const byte getPin();

    /**
     * @brief Funzione per la lettura dello stato del sensore
     * @return stato del sensore
     */
    const Reading getLastReading();

    /** @brief Legge lo stato del sensore di movimento */
    bool isHigh();

    /**
     * @brief Aggiorna l'ultimo stato del sensore
     * @param lastReading ultimo stato del sensore
     */
    void updateLastState(Reading lastReading);
};
#endif //MOVEMENT_SENSOR_H