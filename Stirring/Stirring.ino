
#define power P1_6
#define readsensor P1_3
int motorspeed;
volatile int rpm;
volatile int period;
float analogspeed;
long lastMillis=0;

void setup()
{ 
  Serial.begin(9600);
  pinMode(readsensor,INPUT);
  pinMode(power,OUTPUT);
  attachInterrupt(readsensor,measure,RISING);
  analogspeed=0.0;
  motorspeed=1500;
  rpm=0;
  interrupts();
}

void loop()
{
  Serial.println(rpm);

  if(Serial.available()>0)
    {
      motorspeed=Serial.read();
      
    }
  if(motorspeed<=1500&&motorspeed>=500)
    { 
      if(analogspeed>127)
        {
          analogspeed--;
        }
      else if(rpm<motorspeed)
          {
             analogspeed+=0.08;
             analogWrite(power,analogspeed/2);
          }
      else if(rpm==motorspeed)
          {
            analogWrite(power,analogspeed/2);
          }
      else
          {
            analogspeed-=0.08; 
            analogWrite(power,analogspeed/2);
          }
    }
    else
      analogWrite(power,0);
    
}

void measure()
{
  period=2*(millis() - lastMillis);
  lastMillis=millis();
  rpm=60000/period;
}
