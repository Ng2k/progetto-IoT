#ifndef STATE_H
#define STATE_H

#include "Context.h"
#include "MovementSensor.h"

class Context;

class State {
protected:
    unsigned long _lastTime = millis();
    Reading _lastReading;
    const unsigned int _delayDebounce = 500;
public:
    /**
     * @brief Constructor for State class
     * @param context Pointer to the Context object.
     */
    State();

    /**
     * @brief Funzione per la gestione dei cambi di stato
     * @param context 
    */
    virtual void handle(Context* ctx) = 0;
};

/** @brief Classe per rappresentare lo stato di inattività. */
class IdleState: public State {
public:
	void handle(Context* ctx);
};

/** @brief Classe per rappresentare lo stato di attesa */
class WaitingForTransition: public State {
public:
    void handle(Context* ctx);
};

/** @brief Classe per rappresentare lo stato di ingresso */
class EnterState: public State {
public:
	void handle(Context* ctx);
};

/** @brief Classe per rappresentare lo stato di uscita */
class ExitState: public State {
public:
	void handle(Context* ctx);
};

/** @brief Classe per rappresentare lo stato di errore */
class ErrorState: public State {
public:
    void handle(Context* ctx);
};

#endif // STATE_H