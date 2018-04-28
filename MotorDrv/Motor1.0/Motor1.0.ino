#include <Servo.h> 
 
const int left = 0;
const int right = 1;
const int ENA = 0;
const int in1 = 1;
const int in2 = 2;
Servo ServoL;
Servo ServoR;
const int servoL = 5; ////////////////////////////
const int servoR = 6; ////////////////////////////
int Motor[1][2][2];

void STOP()
{
    digitalWrite(Motor[left][1][in1],0);  digitalWrite(Motor[left][1][in2],0);
    digitalWrite(Motor[right][1][in1],0);  digitalWrite(Motor[right][1][in2],0);
    digitalWrite(Motor[left][2][in1],0);  digitalWrite(Motor[left][2][in2],0);
    digitalWrite(Motor[right][2][in1],0);  digitalWrite(Motor[right][2][in2],0);
}
void BACK(int speed)
{
    //speed = map(speed,0,100,0,255)
    digitalWrite(Motor[left][1][in1],0);  digitalWrite(Motor[left][1][in2],1);
    digitalWrite(Motor[right][1][in1],1);  digitalWrite(Motor[right][1][in2],0);
    digitalWrite(Motor[left][2][in1],0);  digitalWrite(Motor[left][2][in2],1);
    digitalWrite(Motor[right][2][in1],1);  digitalWrite(Motor[right][2][in2],0);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}

void LEFT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(Motor[left][1][in1],0);  digitalWrite(Motor[left][1][in2],1);
    digitalWrite(Motor[right][1][in1],0);  digitalWrite(Motor[right][1][in2],1);
    digitalWrite(Motor[left][2][in1],1);  digitalWrite(Motor[left][2][in2],0);
    digitalWrite(Motor[right][2][in1],1);  digitalWrite(Motor[right][2][in2],0);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}
void RIGHT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(Motor[left][1][in1],1);  digitalWrite(Motor[left][1][in2],0);
    digitalWrite(Motor[right][1][in1],1);  digitalWrite(Motor[right][1][in2],0);
    digitalWrite(Motor[left][2][in1],0);  digitalWrite(Motor[left][2][in2],1);
    digitalWrite(Motor[right][2][in1],0);  digitalWrite(Motor[right][2][in2],1);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}
void TURNLEFT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(Motor[left][1][in1],0);  digitalWrite(Motor[left][1][in2],1);
    digitalWrite(Motor[right][1][in1],0);  digitalWrite(Motor[right][1][in2],1);
    digitalWrite(Motor[left][2][in1],0);  digitalWrite(Motor[left][2][in2],1);
    digitalWrite(Motor[right][2][in1],0);  digitalWrite(Motor[right][2][in2],1);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}
void TURNRIGHT(int speed)
{
    //speed = map(speed,0,100,0,255);
    digitalWrite(Motor[left][1][in1],1);  digitalWrite(Motor[left][1][in2],0);
    digitalWrite(Motor[right][1][in1],1);  digitalWrite(Motor[right][1][in2],0);
    digitalWrite(Motor[left][2][in1],1);  digitalWrite(Motor[left][2][in2],0);
    digitalWrite(Motor[right][2][in1],1);  digitalWrite(Motor[right][2][in2],0);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}

/*
    digitalWrite(Motor[left][1][in1],1);  digitalWrite(Motor[left][1][in2],0);
    digitalWrite(Motor[right][1][in1],1);  digitalWrite(Motor[right][1][in2],0);
    digitalWrite(Motor[left][2][in1],1);  digitalWrite(Motor[left][2][in2],0);
    digitalWrite(Motor[right][2][in1],1);  digitalWrite(Motor[right][2][in2],0);              顺时针转
 */
//
void servo (int ServoPin,int value)  
{
//    ervoWrite(ServoPin,value); //value  0-180
}
void FORWARD(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(Motor[left][1][in1],1);  digitalWrite(Motor[left][1][in2],0);
    digitalWrite(Motor[right][1][in1],0);  digitalWrite(Motor[right][1][in2],1);
    digitalWrite(Motor[left][2][in1],1);  digitalWrite(Motor[left][2][in2],0);
    digitalWrite(Motor[right][2][in1],0);  digitalWrite(Motor[right][2][in2],1);
    analogWrite(Motor[left][1][ENA],speed);  
    analogWrite(Motor[left][2][ENA],speed);
    analogWrite(Motor[right][1][ENA],speed);  
    analogWrite(Motor[right][2][ENA],speed);
}
void setup()
{
  ServoR.attach(servoR);
  ServoL.attach(servoL);
  Motor[left][1][ENA]=3;  Motor[left][1][in1]=22;     Motor[left][1][in2]=23;
  Motor[left][2][ENA]=4;  Motor[left][2][in1]=24;     Motor[left][2][in2]=25;
  Motor[right][1][ENA]=5; Motor[right][1][in1]=26;    Motor[right][1][in2]=27;
  Motor[right][2][ENA]=6; Motor[right][2][in1]=30;    Motor[right][2][in2]=31;
    for(int i=22;i<=29;i++)        pinMode(i,OUTPUT);
    for(int i=3;i<=6;i++)          pinMode(i,OUTPUT);
    
    //Serial.begin(9600);
}
void loop()
{
//    if ( Serial.available())
//    {
//        char* buff = Serial.read();
//        char* first = buff[0];
//        int 
//      switch (first){
//          case "T":
//            Serial.println("fvck you , i am okay");
//            break;
//          case "S":
//            STOP();
//            Serial.println("stopped.");
//            break();
//          case "F":
//            
//        }
//     Serial.flush();
   FORWARD(100);
}
