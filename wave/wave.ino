int NUM_ANGLES = 1;

int lservo = 0;
// Listing of pulse times for different angles. -90/90/0, according to spec sheet.
int pulse[] = {2000, 1000, 1500};

void setup() {
  pinMode(lservo, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while(true) {
    for(int i = 0; i < NUM_ANGLES; i++) {
      digitalWrite(lservo, HIGH);
      Serial.print(pulse[i]);
      delayMicroseconds(pulse[i]);
      digitalWrite(lservo, LOW);
      Serial.print("Waiting.");
      delay(5000); // Wait 5 seconds. 
      Serial.print("Done waiting.");
    }
  }
}
