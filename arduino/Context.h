#ifndef CONTEXT_H
#define CONTEXT_H

#include "State.h"
#include "InfraRed.h"
#include "LedRgb.h"

class State;

class Context {
private:
    State* _contextState;
    InfraRed* _enterSensor;
    InfraRed* _exitSensor;
    LedRgb* _ledRgb;
    unsigned short _peopleCount;
    unsigned long _lastExecutionTime;
    Output _contextOutput;
    //ActuatorManager _actuatorManager;
public:
    /**
     * @brief Constructor for Context class
     *
     * @param state Pointer to the initial state object. The Context object will take ownership of the state object.
     */
    Context(
        State* contextState,
        InfraRed* enterSensor,
        InfraRed* exitSensor,
        LedRgb* ledRgb,
        Output contextOutput,
        //ActuatorManager actuatorManager,
        unsigned short peopleCount,
        unsigned long lastExecutionTime
    );

    /**
     * @brief Funzione per ottenere il sensore di ingresso
     *
     * @return il sensore di ingresso
    */
    InfraRed* getEnterSensor()
    {
        return this->_enterSensor;
    }

    /**
     * @brief Funzione per ottenere il sensore di uscita
     *
     * @return il sensore di uscita
    */
    InfraRed* getExitSensor()
    {
        return this->_exitSensor;
    }

    LedRgb* getLedRgb()
    {
        return this->_ledRgb;
    }

    Output getContextOutput() const { return this->_contextOutput; };
    void setContextOutput(Output contextOutput)
    {
        this->_contextOutput = contextOutput;
    };

    State* getContextState() { return this->_contextState; }
    void setContextState(State* contextState)
    {
        this->_contextState = contextState;
    }

    /**
     * @brief Funzione per ottenere il numero di persone nel contesto
     *
     * @return numero di persone 
    */
    unsigned short getPeopleCount() { return this->_peopleCount; }

    void incrementPeopleCount() { this->_peopleCount++; }
    void decrementPeopleCount() { this->_peopleCount--; }

    /**
     * @brief Funzione per ottenere il numero di ms dall'ultima esecuzione della funzione loop()
     *
     * @return numero di millisecondi dall'ultima esecuzione
    */
    unsigned long getLastExecutionTime()
    {
        return this->_lastExecutionTime;
    }

    /**
     * @brief Funzione per salvare il numero di ms dell'ultima esecuzione della funzione loop()
     *
     * @param lastExecutionTime
    */
    void setLastExecutionTime(unsigned long lastExecutionTime)
    {
        this->_lastExecutionTime = lastExecutionTime;
    }

    /**
    * @brief Funzione per gestire il flusso di operazioni del progetto
    */
    void request();
};
#endif // CONTEXT_H