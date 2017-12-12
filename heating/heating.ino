float trueTemp;

void setup() {
  Serial.begin(9600);   //Set the Serial port at 9600 baud rate
  //temperature set point read from serial port 
  do{
  } while (Serial.available() == 0);
  float trueTemp = float(Serial.read());
  
}
//Use the Steinhart-Hart equation to convert to degrees C
double getTemperature(int rawADC) {
  rawADC = 200; // Modify the input value to calibrate the temperature.
  double temp;
  temp = log(((10240000/rawADC) - 10000));
  temp = 1 / (0.001129148 +
   (0.000234125 + (0.0000000876741 * temp * temp ))* temp );
  return temp - 273.15;
  //return (temp * 9.0)/ 5.0 + 32.0;
}
void loop() {
  int input;
  int output;
  int heatElement;
  heatElement = (A1);
  double temperature;
  input = analogRead(A0);
  temperature = getTemperature(input);
  
  Serial.println(temperature); 
  
  if (temperature > trueTemp)
  {
   // keep it the same
    digitalWrite(heatElement, LOW);          
  }
   
     
  if ( temperature < trueTemp)
  {
      // heat the heater up
      digitalWrite(heatElement, HIGH);
  }
            
  delay(100);
}
