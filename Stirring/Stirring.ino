
#define power P1_6
#define readsensor P1_3
int motorspeed;
volatile int rpm;
volatile int period;
int analogspeed;
long lastMillis=0;

void measure()
{
  period=2*(millis() - lastMillis);
  lastMillis=millis();
  rpm=60000/period;
}

void setup()
{ 
  Serial.begin(9600);
  pinMode(readsensor,INPUT);
  pinMode(power,OUTPUT);
  
//  pinMode(switch1,INPUT_PULLUP);
//  pinMode(switch2,INPUT_PULLUP);
  
  attachInterrupt(readsensor,measure,RISING);
  analogspeed=20;
  do {
  } while (Serial.available()==0);

  motorspeed = Serial.read();
  motorspeed = motorspeed * 20;
  
  rpm=0;
  interrupts();
}


void loop()
{
//  Serial.println(rpm);
  
  if(motorspeed<=1500&&motorspeed>=500)
    { 
      while(analogspeed>127)
        {
          analogspeed=127;
        }
        
      if(rpm<motorspeed)
          {
             analogspeed++;
             analogWrite(power,analogspeed);
          }
      else if(rpm==motorspeed)
          {
            analogWrite(power,analogspeed);
          }
      else
          {
            analogspeed--; 
            analogWrite(power,analogspeed);
          }
    }else{
      analogspeed = 0;
      analogWrite(power,analogspeed);
    }
    
}


