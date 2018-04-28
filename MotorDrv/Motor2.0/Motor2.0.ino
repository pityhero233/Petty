
int MotorL1=3; 
int MotorL2=4; 
int MotorR1=5;
int MotorR2=6;
int SpeedToPWM[256];
int speedL1,speedL2,speedR1,speedR2;
char serialData[18];  //储存信息
int numdata=0;
int mode;
int TargetSpeed;

void setup()
{
    Serial.begin(9600);  
    while(Serial.read()>= 0){}//clear serial port  

    for(int i=22;i<=29;i++)        pinMode(i,OUTPUT);
    for(int i=3;i<=6;i++)          pinMode(i,OUTPUT);
    //Serial.begin(9600);


}

void loop()
{
    ReadMessage();

    FORWARD(50);//test
    delay(1000);
    BACK(50);//test
    delay(1000);
    LEFT(50);//test
    delay(1000);
    RIGHT(50);//test
    delay(1000);
    TURNLEFT(50);//test
    delay(1000);
    TURNRIGHT(50);//test
    delay(1000);
    STOP();//test
    delay(1000);
}


void ReadMessage()
{

    if(Serial.available()>0){  
      delay(10);  /////////////////////////////////////////////////////////////
      numdata = Serial.readBytes(serialData,9);  
      Serial.println("Serial.readBytes:");  
     
      mode = serialData[0]-'0';  
      TargetSpeed = (serialData[2]-'0') * 100 + (serialData[3]-'0') * 10 + (serialData[4]-'0') * 1 ;
     
      //第1位  模式（直走 倒退  左转 balabala
      //第3、4、5 位   目标速度
      //第7、8、9位  待定（可能是捡球机构、弹射机构的控制
      
      Serial.println(mode);       //  
      Serial.println(TargetSpeed);  
      //Serial.println(serialData); 
    }  
  while(Serial.read() >= 0){}  
  for(int i=0; i<18; i++)  serialData[i]='\0'; // clear serial buffer   
}


void TEST(int speed)
{
   // speed = map(speed,0,100,0,255);
   
    digitalWrite(22,1);    digitalWrite(26,0);
    digitalWrite(23,0);    digitalWrite(27,1);
    
    digitalWrite(24,1);    digitalWrite(28,0);
    digitalWrite(25,0);    digitalWrite(29,1);
    
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);   
    analogWrite(MotorR2,speed);
    delay(10);
}
void FORWARD(int speed)
{
   // speed = map(speed,0,100,0,255);
   
    digitalWrite(22,1);   digitalWrite(26,0);
    digitalWrite(23,0);   digitalWrite(27,1);
    
    digitalWrite(24,1);   digitalWrite(28,0); 
    digitalWrite(25,0);   digitalWrite(29,1);
     
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
   analogWrite(MotorR1,speed);   
    analogWrite(MotorR2,speed);
    delay(10);
}
void STOP()
{
    digitalWrite(22,0);   digitalWrite(26,0);
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,0);
    digitalWrite(25,0);   digitalWrite(29,0);
      
      
      
    delay(10);
    
}
void BACK(int speed)
{
    //speed = map(speed,0,100,0,255)
    digitalWrite(22,0);   digitalWrite(26,1);
    digitalWrite(23,1);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,1);
    digitalWrite(25,1);   digitalWrite(29,0);
  
      
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);  
    analogWrite(MotorR2,speed);
    delay(10);
}
void LEFT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,0);   digitalWrite(26,0); 
    digitalWrite(23,1);   digitalWrite(27,1);
    
    digitalWrite(24,1);   digitalWrite(28,1); 
    digitalWrite(25,0);   digitalWrite(29,0);
     
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);  
    analogWrite(MotorR2,speed);
    delay(5);
}
void RIGHT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,1);   digitalWrite(26,1); 
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,0);  
    digitalWrite(25,1);   digitalWrite(29,1);
    
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);  
    analogWrite(MotorR2,speed);
    delay(10);
}
void TURNLEFT(int speed)
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,0);   digitalWrite(26,0); 
    digitalWrite(23,1);   digitalWrite(27,1);
    
    digitalWrite(24,0);   digitalWrite(28,0); 
    digitalWrite(25,1);   digitalWrite(29,1);

    
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);  
    analogWrite(MotorR2,speed);
    delay(10);
}
void TURNRIGHT(int speed)
{
    //speed = map(speed,0,100,0,255);
    digitalWrite(22,1);   digitalWrite(26,1);  
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,1);   digitalWrite(28,1); 
    digitalWrite(25,0);   digitalWrite(29,0);
  
    
    analogWrite(MotorL1,speed);  
    analogWrite(MotorL2,speed);
    analogWrite(MotorR1,speed);  
    analogWrite(MotorR2,speed);
    delay(10);
}
