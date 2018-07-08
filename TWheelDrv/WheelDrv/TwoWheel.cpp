#include"Arduino.h"
#include"TwoWheel.h"
unsigned long now = 0;
unsigned long past = 0;
int LWhlChngNow = 0,RWhlChngNow = 0;//Interrupt change count
/*TODO:
    int TwoWheel::GetLSpeed() 
    输出记得map一下 map(0,b,0,100);

TODO:
    GetLSpeed GetRSpeed 务必定时执行
*/
struct WheelChangeCount
{
    int WhlCntNow ;
    int WhlCntPast ;//Interrupt change count
};
WheelChangeCount LCnt,Rcnt;
int LSpeed,RSpeed;

TwoWheel::LCount()
{
    LCnt.WhlCntNow++;
}
TwoWheel::RCount()
{
    RCnt.WhlCntNow++;
}
void TwoWheel::WrtSpd(bool LDirection,byte LSpd,bool RDirection,byte RSpd)
{

}
void TwoWheel::WrtCircle((bool LDirection ,byte LCircle,bool RDirection,byte RCircle)
{

}
void TwoWheel::InitWheel(byte LWhlENAPin,byte LWhlIn1Pin,byte LWhlIn2Pin,byte LIntrrptPin,
                       byte RWhlENAPin,byte RWhlIn1Pin,byte RWhlIn2Pin,byte RIntrrptPin)//LENA  LIn1  LIn2 LIntrrpt RENA  RIn1 RIn2  RIntrrpt
{
    pinMode(LWhlENAPin,OUTPUT);
    pinMode(LWhlIn1Pin,OUTPUT);
    pinMode(LWhlIn2Pin,OUTPUT);
    pinMode(LIntrrptPin,INPUT);
    pinMode(RWhlENAPin,OUTPUT);
    pinMode(RWhlIn1Pin,OUTPUT);
    pinMode(RWhlIn2Pin,OUTPUT);
    pinMode(RIntrrptPin,INPUT);
    LCnt.WhlCntNow = 0;
    LCnt.WhlCntPast = 0;
    RCnt.WhlCntNow = 0;
    RCnt.WhlCntPast = 0;
    attachInterrupt(digitalPinToInterrupt(LIntrrptPin), LCount, CHANGE);
    attachInterrupt(digitalPinToInterrupt(RIntrrptPin), RCount, CHANGE);
}

int TwoWheel::GetLSpeed()   //time  per second
{
    int LSpeed = (LCnt.WhlCntNow-LCnt.WhlCntPast)  ;
    LCnt.WhlCntPast = Lcnt.WhlCntNow;

    return LSpeed;
}
int TwoWheel::GetRSpeed()   //time  per second
{
    int RSpeed = (RCnt.WhlCntNow-RCnt.WhlCntPast);
    RCnt.WhlCntPast = Rcnt.WhlCntNow;

    return RSpeed;
}
