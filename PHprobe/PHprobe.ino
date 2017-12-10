int PinBase = P2_4;
int PinAcid = P2_5;
int Pin = A5;
float F = 9.6485309*pow(10,4);
float R = 8.314510;
float T = 298;
boolean addBase;
boolean addAcid;
float maintainPH = 5;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(Pin, INPUT);
  pinMode(PinAcid, OUTPUT);
  pinMode(PinBase, OUTPUT);
  do {
  } while (Serial.available()==0);
  maintainPH = Serial.read();
}


float calculatePH() {
  float volt = 1.65 - (3.3 / 1024) * (analogRead(Pin));
  float PH = 7 + ((volt*F) / (R * T * logf(10)));
  return PH;
}
  
  
  
void loop()
{
    
    if (calculatePH() < (maintainPH - 0.5)) {
      while(calculatePH() < maintainPH) {
        analogWrite(PinBase, 180);
        Serial.println(calculatePH());
        delay(100);
      }
    }
    analogWrite(PinBase, 0);
        
    if (calculatePH() > (maintainPH + 0.5)) {
       while(calculatePH() > maintainPH){
         analogWrite(PinAcid, 180);
         Serial.println(calculatePH());
         delay(100);
       }
     }
     analogWrite(PinAcid, 0);
    
}
