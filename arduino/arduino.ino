/**
 * @file arduino.ino
 * @brief Controllo di un LED RGB tramite pulsanti utilizzando il pattern State.
 *
 * Questo programma controlla un LED RGB utilizzando due pulsanti per cambiare il colore del LED
 * in base allo stato attuale, implementato con il pattern State.
 *
 * Per simulare ingressi e uscite è stato usato un LED RGB per rappresentare lo stato:
 * 		- blu: stato di attesa/idle
 * 		- verde: ingresso di una persona
 * 		- rosso: uscita di una persona
 *
 * Il programma è stato sviluppato per Arduino Nano 33 IoT e Arduino Mega.
 *
 * @version 1.0
 * @author Nicola Guerra
 * @author Tommaso Mortara
 */

#include <Arduino.h>

// Pin del LED RGB
const byte ledRGBPins[3] = { 11, 9, 10 };

// Pin dei pulsanti
const byte enterButtonPin = 2;
const byte exitButtonPin = 4;

// Colori RGB per diversi stati
const byte idleRGB[3] = { 0, 0, 255 };
const byte exitRGB[3] = { 255, 0, 0 };
const byte enterRGB[3] = { 0, 255, 0 };

// Frequenza di campionamento in millisecondi
const unsigned int FREQUENCY = 1000;

/**
 * @enum BtnInput
 * @brief Stati del pulsante.
 */
enum ButtonState { PRESSED, RELEASED };

/**
 * @enum Output
 * @brief Stati di output per controllare l'attuatore (LED RGB).
 */
enum Output { OFF, ENTER, EXIT };

/**
 * @brief Classe astratta per rappresentare uno stato.
 */
class State {
public:
    virtual void handle(Context* context) = 0;
};

/**
 * @brief Classe contesto che mantiene lo stato corrente.
 */
class Context {
private:
    State* currentState;
	ButtonState* enterButtonState;
	ButtonState* exitButtonState;
	unsigned short peopleCounter;
	unsigned long lastExecution;
public:
    Context(State* state) : 
		currentState(state), 
		enterButtonState(RELEASED), 
		exitButtonState(RELEASED), 
		peopleCount(0), 
		lastExecution(millis()) {}

    void setState(State* state) {
        currentState = state;
    }

    void request() {
        currentState->handle(this);
    }

	/**
	 * @brief Imposta il colore del LED RGB.
	 *
	 * Questa funzione imposta il colore del LED RGB usando i valori RGB forniti.
	 * Attenzione:	I valori devono essere compresi tra 0 e 255.
	 *				La funzione, inoltre assume che l'ordine dei valori sia:
	 *			   	-> [R (Red/Rosso), G (Green/Verde), B (Blue/Blu)].
	 *
	 * @param rgbPins Array dei pin del LED RGB.
	 * @param rgbValues Array dei valori RGB da impostare.
	 */
    void setRGBLedColor(const byte rgbValues[3]) {
        for(unsigned char i = 0; i < 3; i++) {
            analogWrite(ledRGBPins[i], rgbValues[i]);
        }
    }
};

/**
 * @brief Classe per rappresentare lo stato di inattività.
 */
class IdleState : public State {
public:
    void handle(Context* context)
	{
		context->setRGBLedColor(idleRGB);
		context->enterButtonState = RELEASED;
		context->exitButtonState = RELEASED;

		if(
			digitalRead(enterButtonPin) == HIGH &&
			digitalRead(exitButtonPin) == LOW
		) {
			context->setState(new ReadInIdleState());
		}
		else if(
			digitalRead(enterButtonPin) == LOW &&
			digitalRead(exitButtonPin) == HIGH &&
			context->peopleCount > 0
		) {
			context->setState(new ReadOutIdleState());
		}
	}
};

/**
 * @brief Classe per rappresentare lo stato di lettura inattivo.
 */
class ReadInIdleState : public State {
public:
	void handle(Context* context)
	{
		context->setRGBLedColor(idleRGB);
		context->enterButtonState = PRESSED;
		context->exitButtonState = RELEASED;

		if(
			digitalRead(enterButtonPin) == LOW &&
			digitalRead(exitButtonPin) == HIGH
		) {
			context->setState(new EnterState());
			return;
		}

		context->setState(new IdleState());
	}
};

/**
 * @brief Classe per rappresentare lo stato di lettura inattivo.
 */
class ReadOutIdleState : public State {
public:
	void handle(Context* context)
	{
		context->setRGBLedColor(idleRGB);
		context->enterButtonState = RELEASED;
		context->exitButtonState = PRESSED;

		if(
			digitalRead(enterButtonPin) == HIGH &&
			digitalRead(exitButtonPin) == LOW &&
			context->peopleCount > 0
		) {
			context->setState(new ExitState());
			return;
		}

		context->setState(new IdleState());
	}
};

/**
 * @brief Classe per rappresentare lo stato di ingresso.
 */
class EnterState : public State {
public:
    void handle(Context* context)
	{
		context->setRGBLedColor(enterRGB);
		context->exitButtonState = PRESSED;
		context->peopleCount++;

		// todo: chiedere al prof come togliere il delay()
		delay(1000); 
		context->setState(new IdleState());
	}
}

/**
 * @brief Classe per rappresentare lo stato di uscita.
 */
class ExitState : public State {
public:
    void handle(Context* context)
	{
		context->setRGBLedColor(exitRGB);
		context->enterButtonState = PRESSED;
		context->peopleCount--;

 		// todo: chiedere al prof come togliere il delay()
		delay(1000);
		context->setState(new IdleState());
	}
};

// Contesto del sistema
Context* context;

void setup() {
    for(const byte pin : ledRGBPins) {
        pinMode(pin, OUTPUT);
    }
    pinMode(btnInPin, INPUT);
    pinMode(btnOutPin, INPUT);

    context = new Context(new IdleState());
    Serial.begin(9600);
}

/**
 * @brief Funzione di loop eseguita continuamente.
 */
void loop() {
	if(context->lastExecution - millis() < FREQUENCY) {
		return;
	}

    context->request();
	context->lastExecution = millis();
}