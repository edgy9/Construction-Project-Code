#include <ArduinoJson.h>
#include <Stepper.h>

StaticJsonDocument<100> outgoing;
StaticJsonDocument<900> incoming;
StaticJsonDocument<100> blindstate;

const int UpdateStepResolution = 20;
const int StepsPerRevolution = 2048;



Stepper SittingRoomBlind = Stepper(StepsPerRevolution, 8, 10, 9, 11);

const int feedbackInterval = 100;
int CurrentPosition = 0;

void setup() {
  // Set the speed of the stepper motor
  SittingRoomBlind.setSpeed(60); // Set the speed to 60 RPM

  Serial.begin(115200);
  while (!Serial);
  
  pinMode(13, OUTPUT)
  pinMode(4, OUTPUT)
  pinMode(5, OUTPUT)
  pinMode(6, OUTPUT)

  // Initialize the stepper motor to the initial position
  MoveBlind("sitting-room", 0);
  delay(1000); // Wait for a second
}

void loop() {
  if (Serial.available()) {
    DeserializationError error = deserializeJson(incoming, Serial);

    if (error); //outgoing["msg"] = "Arduino Error: " + String(error.c_str());
  
    else if (incoming["msg"] == "REQ") {
      outgoing["msg"] = "ACK";
      
     
        serializeJson(outgoing, Serial);
        Serial.print('\n');
        if (incoming["device_type"] == "blinds"){
            int RotPosition = incoming["value"];
            MoveBlind(incoming["entity"], RotPosition);
        }
        if (incoming["device_type"] == "lights"){
            ToggleLight(incoming["pin"], incoming["state"]);
        }
    }
  }
}

void ToggleLight(int pin_number, bool state) {
    digitalWrite(pin_number, state ? HIGH | LOW)
    

}



void MoveBlind(String entity, int TargetPosition) {
  // Calculate the number of steps to move
  int StepsToMove = TargetPosition - CurrentPosition;
  int StepsTaken = 0;
  if (StepsToMove > 0) {
    while (StepsToMove > StepsTaken) {
    // Move the stepper motor
    SittingRoomBlind.setSpeed(5);
    SittingRoomBlind.step(UpdateStepResolution);
    StepsTaken = StepsTaken + UpdateStepResolution;
    // Update the current position
    
  
    // Provide feedback on the current position
    //Serial.print("Current Position: ");
    //Serial.println(currentPosition + stepsTaken);
    blindstate["msg"] = "state";
    blindstate["entity"] = "sitting-room-blind-state";
    blindstate["value"] = (CurrentPosition + StepsTaken);
    serializeJson(blindstate, Serial);
    Serial.print('\n');
    }
  }
  else if (StepsToMove < 0){
    while (StepsToMove < StepsTaken) {
    // Move the stepper motor
    SittingRoomBlind.setSpeed(5);
    SittingRoomBlind.step(- UpdateStepResolution);
    StepsTaken = StepsTaken - UpdateStepResolution;
    // Update the current position
    
  
    // Provide feedback on the current position
    //Serial.print("Current Position: ");
    //Serial.println(currentPosition + stepsTaken);
    blindstate["msg"] = "state";
    blindstate["entity"] = "sitting-room-blind-state";
    blindstate["value"] = (CurrentPosition + StepsTaken);
    serializeJson(blindstate, Serial);
    Serial.print('\n');
    }
  }

  // Delay to provide feedback interval
  CurrentPosition = CurrentPosition + StepsTaken;
  delay(feedbackInterval);
}