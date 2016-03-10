/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
const int C1B = 12;
const int C1A = 8;
const int C2B = 4;
const int C2A = 2;
const int EN1 = 13;
const int EN2 = 7;

char data;
// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  Serial.begin(9600);
  pinMode(C1A, OUTPUT);     
  pinMode(C1B, OUTPUT);
  pinMode(C2A, OUTPUT);
  pinMode(C2B, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(EN1, OUTPUT);
}

void start()
{
  digitalWrite(EN2, HIGH);   
  digitalWrite(EN1, HIGH);   
}

void turn_left()
{
  start();
  digitalWrite(C1A, LOW);   
  digitalWrite(C1B, LOW);   
  digitalWrite(C2A, LOW);   
  digitalWrite(C2B, HIGH);  
}

void turn_right()
{
  start();
  digitalWrite(C1A, LOW);   
  digitalWrite(C1B, LOW);   
  digitalWrite(C2A, HIGH);  
  digitalWrite(C2B, LOW);   
}

void fwd()
{
  start();
  digitalWrite(C1A, LOW);   
  digitalWrite(C1B, HIGH);  
  digitalWrite(C2A, LOW);   
  digitalWrite(C2B, HIGH);  
}

void back()
{
  start();
  digitalWrite(C1A, HIGH);  
  digitalWrite(C1B, LOW);   
  digitalWrite(C2A, HIGH);  
  digitalWrite(C2B, LOW);   
}

void Stop()
{
  /*
  digitalWrite(C1A, LOW);   
  digitalWrite(C1B, LOW);   
  digitalWrite(C2A, LOW);   
  digitalWrite(C2B, LOW);   
  */
  
  digitalWrite(EN1, LOW);   
  digitalWrite(EN2, LOW);   
}

void loop() {
  if(Serial.available()>0)
  {
    data = Serial.read();
    
    Serial.println(data);
    
    switch(data)
    {
      case 'l':
              turn_left();
              delay(10);    
              Stop();
              break;
      case 'r':
              turn_right();
              delay(10);    
              Stop();
              break;
      
      case 'f':
              fwd();
              delay(10);    
              Stop();
              break;
      case 'b':
              back();
              delay(10);    
              Stop();
              break;
      
    }
  }
}
