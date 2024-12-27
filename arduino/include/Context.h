#ifndef CONTEXT_H
#define CONTEXT_H

#include "header.h"
#include "LedRgb.h"
#include "MovementSensor.h"
#include "State.h"

class State;

class Context {
public:
    /** @brief Constructor for Context class */
    Context(
        State* contextState,
        MovementSensor* enterSensor,
        MovementSensor* exitSensor,
        LedRgb* ledRgb
    );

    /**
     * @brief Funzione per ottenere il sensore di ingresso
     * @return il sensore di ingresso
     */
    MovementSensor* getEnterSensor() { return this->_enterSensor; }

    /**
     * @brief Funzione per ottenere il sensore di uscita
     * @return il sensore di uscita
     */
    MovementSensor* getExitSensor() { return this->_exitSensor; }

    /**
     * @brief Funzione per ottenere il LED RGB
     * @return il LED RGB
     */
    LedRgb* getLedRgb() { return this->_ledRgb; }

    /**
     * @brief Funzione per ottenere l'output del contesto
     * @return l'output del contesto
     */
    Output getContextOutput() const { return this->_contextOutput; };

    /**
     * @brief Funzione per impostare l'output del contesto
     * @param output output del contesto
     */
    void setContextOutput(Output output) { this->_contextOutput = output; };

    /**
     * @brief Funzione per ottenere lo stato del contesto
     * @return lo stato del contesto
     */
    State* getContextState() { return this->_contextState; }

    /**
     * @brief Funzione per impostare lo stato del contesto
     * @param state stato del contesto
     */
    void setContextState(State* state) { this->_contextState = state; }

    /**
     * @brief Funzione per ottenere il numero di persone nel contesto
     * @return numero di persone 
     */
    int getPeopleCount() { return this->_peopleCount; }

    /** @brief Funzione per incrementare il numero di persone nel contesto */
    void incrementPeopleCount() { this->_peopleCount++; }

    /** @brief Funzione per decrementare il numero di persone nel contesto */
    void decrementPeopleCount() { this->_peopleCount--; }

    /** @brief Funzione per gestire il flusso di operazioni del progetto */
    void request();
private:
    int _peopleCount;
    Output _contextOutput;
    State* _contextState;
    MovementSensor* _enterSensor;
    MovementSensor* _exitSensor;
    LedRgb* _ledRgb;
};
#endif // CONTEXT_H