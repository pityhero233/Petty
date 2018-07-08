#include"Arduino.h"
#include "TwoWheel.h"
#define TimeInterval 50
void setup()
{

    InitWheel();//TODO: input pin
    Serial.begin(19200);

}
void loop()
{
    
    now = millis();
    if ( (now - past) >= TimeInterval)//run once per TimeInterval
    {













    }
}