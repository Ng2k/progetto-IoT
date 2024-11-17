// C++ code
//
const byte ledRGBPins[3] = { 11, 9, 10 };
const byte btnInPin = 2;
const byte btnOutPin = 4;

const byte idleRGB[3] = { 0, 0, 255 };
const byte exitRGB[3] = { 255, 0, 0 };
const byte enterRGB[3] = { 0, 255, 0 };

// frequenza campionamento ingressi
const unsigned int FREQUENCY = 1000;

// States:
enum State {
	IDLE,
	READ_IN_IDLE, READ_IN_INCOMPLETE,
	IN,
	READ_OUT_IDLE, READ_OUT_INCOMPLETE,
	OUT
};

// inputs:
enum ButtonInput { PRESSED, RELEASED };

// outputs:
enum Output { OFF, ENTER, EXIT };

State iCurrentState;
ButtonInput iBtnInput;
ButtonInput iBtnOutput;
unsigned long lastTime;
unsigned short crowdCounter;

void setRGBLedColor(const byte rgbPins[3], const byte rgbValues[3])
{
	analogWrite(rgbPins[0], rgbValues[0]);
	analogWrite(rgbPins[1], rgbValues[1]);
	analogWrite(rgbPins[2], rgbValues[2]);
}

void setup()
{
	for(const byte pin : ledRGBPins) {
		pinMode(pin, OUTPUT);
	}
	
	pinMode(btnInPin, INPUT);
	pinMode(btnOutPin, INPUT);
	
	iCurrentState = IDLE; // set the initial state

	iBtnInput = RELEASED;
	iBtnOutput = RELEASED;

	crowdCounter = 0;
	
	setRGBLedColor(ledRGBPins, idleRGB);
	
	Serial.begin(9600);

	lastTime = millis();  
}

void loop()
{
	if (millis() - lastTime < FREQUENCY) {
		return;
	}

	// Function F (future state)
	State iFutureState;
	iFutureState = iCurrentState; // default: same state
	
	Serial.println("-----------------------------------------");
	
	//Stati: A->A, B->A
	bool isIdle = (
		(iCurrentState == IDLE) && (iBtnInput == RELEASED && iBtnOutput == RELEASED)
	);
	bool isMultipleIn = (
		(iCurrentState == READ_IN_IDLE) &&
		(
			(iBtnInput == PRESSED && digitalRead(btnInPin) == HIGH) &&
			iBtnOutput == RELEASED
		)
	);
	bool isMultipleOut = (
		(iCurrentState == READ_OUT_IDLE) &&
		(
			(iBtnOutput == PRESSED && digitalRead(btnOutPin) == HIGH) &&
			iBtnInput == RELEASED
		)
	);
	
	if(isIdle || isMultipleIn || isMultipleOut) {
		iBtnInput = RELEASED;
		iBtnOutput = RELEASED;
		iFutureState = IDLE;
		Serial.println("IDLE");
	}

	//Stato: A->B
	if (
		(iCurrentState == IDLE) &&
		(digitalRead(btnInPin) == HIGH && iBtnOutput == RELEASED)
	)
	{
		iFutureState = READ_IN_IDLE;
		iBtnInput = PRESSED;
		Serial.println("READ_IN_IDLE");
	}
	
	//Stato: B->B
	if(
		(iCurrentState == READ_IN_IDLE) &&
		(iBtnInput == PRESSED && iBtnOutput == RELEASED)
	)
	{
		iFutureState = READ_IN_IDLE;
		Serial.println("READ_IN_IDLE");
	}
	
	//Stato: B->IN
	if (
		(iCurrentState == READ_IN_IDLE) &&
		(iBtnInput == PRESSED && digitalRead(btnOutPin) == HIGH)
	)
	{
		iFutureState = IN;
		iBtnOutput = PRESSED;
		crowdCounter++;
		Serial.println("IN");
		Serial.print("crowdCounter: ");
		Serial.println(crowdCounter);
	}
	
	//Stato IN/OUT->A
	//todo: frequenza campionamento realistico per evitare 1000 rilevazioni in = 1 out = 1
	if ((iCurrentState == IN) || (iCurrentState == OUT)) {
		Serial.println("IDLE");
		iBtnOutput = RELEASED;
		iBtnInput = RELEASED;
		iFutureState = IDLE;
	}
	
	//Stato: A->E
	if (
		(iCurrentState == IDLE) &&
		(iBtnInput == RELEASED && digitalRead(btnOutPin) == HIGH)  &&
		crowdCounter > 0
	)
	{
		iFutureState = READ_OUT_IDLE;
		iBtnOutput = PRESSED;
		Serial.println("READ_OUT_IDLE");
	}
	
	//Stato: E->E
	if(
		(iCurrentState == READ_OUT_IDLE) &&
		(iBtnInput == RELEASED && iBtnOutput == PRESSED)
	)
	{
		Serial.println("READ_OUT_IDLE");
	}
	
	//Stato: E->OUT
	if (
		(iCurrentState == READ_OUT_IDLE) &&
		(digitalRead(btnInPin) == HIGH && iBtnOutput == PRESSED) &&
		crowdCounter > 0
	)
	{
		iFutureState = OUT;
		iBtnInput = PRESSED;
		crowdCounter--;
		Serial.println("OUT");
		Serial.print("crowdCounter: ");
		Serial.println(crowdCounter);
	}

	// state transition
	iCurrentState = iFutureState;
	
	Output output;
	if (
		iCurrentState == IDLE ||
		iCurrentState == READ_IN_IDLE ||
		iCurrentState == READ_OUT_IDLE
	)
	{
		output = OFF;
	}
	if (iCurrentState == IN) output = ENTER;
	if (iCurrentState == OUT) output = EXIT;  
	
	//  output symbols -> actuators
	if (output == ENTER) setRGBLedColor(ledRGBPins, enterRGB);  
	if (output == OFF) setRGBLedColor(ledRGBPins , idleRGB);
	if (output == EXIT) setRGBLedColor(ledRGBPins , exitRGB);

	lastTime = millis();
}
