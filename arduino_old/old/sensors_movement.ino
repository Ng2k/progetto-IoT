// C++ code
//
const byte ledRGBPins[3] = { 11, 9, 10 };
const byte pirInPin = 2;
const byte pirOutPin = 4;

const byte idleRGB[3] = { 0, 0, 255 };
const byte exitRGB[3] = { 255, 0, 0 };
const byte enterRGB[3] = { 0, 255, 0 };

// frequenza campionamento ingressi
const unsigned int FREQUENCY = 1000;

// States:
enum State {
	IDLE,
	READ_IN_IDLE,
	READ_IN_INCOMPLETE,
	IN,
	READ_OUT_IDLE,
	READ_OUT_INCOMPLETE,
	OUT
};

// inputs:
enum PirRead { MOVEMENT, STATIC };

// outputs:
enum Output { OFF, ENTER, EXIT };

State iCurrentState;
PirRead iPirInput;
PirRead iPirOutput;
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
	
	pinMode(pirInPin, INPUT);
	pinMode(pirOutPin, INPUT);
	
	iCurrentState = IDLE; // set the initial state

	iPirInput = STATIC;
	iPirOutput = STATIC;

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
		(iCurrentState == IDLE) && (iPirInput == STATIC && iPirOutput == STATIC)
	);
	bool isMultipleIn = (
		(iCurrentState == READ_IN_IDLE) &&
		(
			(iPirInput == MOVEMENT && digitalRead(pirInPin) == HIGH) &&
			iPirOutput == STATIC
		)
	);
	bool isMultipleOut = (
		(iCurrentState == READ_OUT_IDLE) &&
		(
			(iPirOutput == MOVEMENT && digitalRead(pirOutPin) == HIGH) &&
			iPirInput == STATIC
		)
	);
	
	if(isIdle || isMultipleIn || isMultipleOut) {
		iPirInput = STATIC;
		iPirOutput = STATIC;
		iFutureState = IDLE;
		Serial.println("IDLE");
	}

	//Stato: A->B
	if (
		(iCurrentState == IDLE) &&
		(digitalRead(pirInPin) == HIGH && iPirOutput == STATIC)
	)
	{
		iFutureState = READ_IN_IDLE;
		iPirInput = MOVEMENT;
		Serial.println("READ_IN_IDLE");
	}
	
	//Stato: B->B
	if(
		(iCurrentState == READ_IN_IDLE) &&
		(iPirInput == MOVEMENT && iPirOutput == STATIC)
	)
	{
		iFutureState = READ_IN_IDLE;
		Serial.println("READ_IN_IDLE");
	}
	
	//Stato: B->IN
	if (
		(iCurrentState == READ_IN_IDLE) &&
		(iPirInput == MOVEMENT && digitalRead(pirOutPin) == HIGH)
	)
	{
		iFutureState = IN;
		iPirOutput = MOVEMENT;
		crowdCounter++;
		Serial.println("IN");
		Serial.print("crowdCounter: ");
		Serial.println(crowdCounter);
	}
	
	//Stato IN/OUT->A
	//todo: frequenza campionamento realistico per evitare 1000 rilevazioni in = 1 out = 1
	if ((iCurrentState == IN) || (iCurrentState == OUT)) {
		Serial.println("IDLE");
		iPirOutput = STATIC;
		iPirInput = STATIC;
		iFutureState = IDLE;
	}
	
	//Stato: A->E
	if (
		(iCurrentState == IDLE) &&
		(iPirInput == STATIC && digitalRead(pirOutPin) == HIGH)  &&
		crowdCounter > 0
	)
	{
		iFutureState = READ_OUT_IDLE;
		iPirOutput = MOVEMENT;
		Serial.println("READ_OUT_IDLE");
	}
	
	//Stato: E->E
	if(
		(iCurrentState == READ_OUT_IDLE) &&
		(iPirInput == STATIC && iPirOutput == MOVEMENT)
	)
	{
		Serial.println("READ_OUT_IDLE");
	}
	
	//Stato: E->OUT
	if (
		(iCurrentState == READ_OUT_IDLE) &&
		(digitalRead(pirInPin) == HIGH && iPirOutput == MOVEMENT) &&
		crowdCounter > 0
	)
	{
		iFutureState = OUT;
		iPirInput = MOVEMENT;
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
}