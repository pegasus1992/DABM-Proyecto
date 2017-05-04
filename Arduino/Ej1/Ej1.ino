void setup() {
  // put your setup code here, to run once:
  pinMode(12,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  //1 estado alto o prendido
  //12 Puerto
  digitalWrite(12, HIGH);
  //En milisegundos QUe espere
  delay(100);
  digitalWrite(12, LOW);
  delay(100);
}
