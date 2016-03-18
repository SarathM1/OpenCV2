#include<Wire.h>

static byte rawData[6];
char result1;
char result2;
char prevRes;
char curRes;
char finRes;

void setup()
{
  Serial.begin(9600);
  i2c_init();
}

void loop()
{
  i2c_read();
  i2c_read_init();
  int joyX  = rawData[0];
  int joyY = rawData[1];
  int accelX = rawData[2];
  int accelY = rawData[3];
  int accelZ = rawData[4] ;
  int btnZ = bitRead(rawData[5],0);
  int btnC = bitRead(rawData[5],1);
  
  
  result1 = check(joyX,78,176,'l','r','s');
  result2 = check(joyY,78,176,'b','f','s');
  
  if (result1 != 's')
     curRes = result1;
  else
     curRes = result2;
  
  if (prevRes != curRes)
  {
      finRes = curRes;
      Serial.println(finRes);
  }
  
  prevRes = curRes;
  //delay(500);
  
}

char check(int val,int x,int y,char str1,char str2,char str3)
{
  char res;
  if(val <= x)
    res = str1;
  else if(val >= y)
    res = str2;
  else
    res = str3; 

  return res;
}

void i2c_read()
{
  int i = 0;
  Wire.requestFrom(0x52,6);
  while(Wire.available())
  {
    rawData[i++] = wii_decode(Wire.read());    
  }
  i2c_read_init();
}

void i2c_init()
{
  Wire.begin();
  Wire.beginTransmission(0x52);
  Wire.write((byte)0x40);
  Wire.write((byte)0x00);
  Wire.endTransmission();
}

void i2c_read_init()
{
  Wire.beginTransmission(0x52);
  Wire.write((byte)0x00);
  Wire.endTransmission();
}

static char wii_decode(byte data)
{
  return ((data^0x17)+0x17);
}

