float sensorValue = 0;
float sensor;

void setup() {
  // put your setup code here, to run once:
  //BitsPirSegundos a los que quiero transmitir 9600 BPS
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(A0); // read the value from the sensor
  sensor = (sensorValue * 500) / 1024;
  Serial.println(sensor); // prints the values coming from the sensor on the screen
}
