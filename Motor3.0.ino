#include <PID_v1.h>
int MotorL1=3; 
int MotorL2=4; 
int MotorR1=5;
int MotorR2=6;
int SpeedToPWM[256];
double speedL1,speedL2,speedR1,speedR2;
double PWML1,PWML2,PWMR1,PWMR2;
int InterruptL1 = 5; //pin 18
int InterruptL2 = 4; //pin 19
int InterruptR1 = 3; //pin 20
int InterruptR2 = 2; //pin 21

char serialData[18];  //储存信息
int numdata=0;
int mode;              // 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT
                    //TODO:7->SHOOT 8->PICK
double TargetSpeed;

unsigned long previousMillis = 0 ;

double Kp=0.4, Ki=5.5, Kd=0; 
PID PID_L1(&speedL1, &PWML1, &TargetSpeed, Kp, Ki, Kd, DIRECT); 
PID PID_L2(&speedL2, &PWML2, &TargetSpeed, Kp, Ki, Kd, DIRECT); 
PID PID_R1(&speedR1, &PWMR1, &TargetSpeed, Kp, Ki, Kd, DIRECT); 
PID PID_R2(&speedR2, &PWMR2, &TargetSpeed, Kp, Ki, Kd, DIRECT); 

void ReadSpeedL1()  {
  speedL1++;
}
void ReadSpeedR1()  {
  speedR1++;
}
void ReadSpeedL2()  {
  speedL2++;
}
void ReadSpeedR2()  {
  speedR2++;
}

void setup()
{
    Serial.begin(57600);  
    while(Serial.read()>= 0){}//clear serial port  

    for(int i=22;i<=29;i++)        pinMode(i,OUTPUT);
    for(int i=3;i<=6;i++)          pinMode(i,OUTPUT);
    //Serial.begin(9600);
    attachInterrupt(InterruptL1 , ReadSpeedL1, CHANGE);
    attachInterrupt(InterruptR1 , ReadSpeedR1, CHANGE);
    attachInterrupt(InterruptL2 , ReadSpeedL2, CHANGE);
    attachInterrupt(InterruptR2 , ReadSpeedR2, CHANGE);

    PID_L1.SetMode(AUTOMATIC);//设置PID为自动模式
    PID_L1.SetSampleTime(50);//设置PID采样频率为100ms
    PID_L2.SetMode(AUTOMATIC);//设置PID为自动模式
    PID_L2.SetSampleTime(50);//设置PID采样频率为100ms
    PID_R1.SetMode(AUTOMATIC);//设置PID为自动模式
    PID_R1.SetSampleTime(50);//设置PID采样频率为100ms
    PID_R2.SetMode(AUTOMATIC);//设置PID为自动模式
    PID_R2.SetSampleTime(50);//设置PID采样频率为100ms

    // MsTimer2::set(100, Speed);        // 中断设置函数，每 100ms 进入一次中断
    // MsTimer2::start();                //开始计时
}

void loop()
{
//  digitalWrite(22,1);  delay(10);
//      digitalWrite(23,0); delay(10);
//            analogWrite(3,55);  delay(10);

    unsigned long currentMillis = millis (); 
    if(Serial.available()>0){  
      ReadMessage();
    }
    else{
         
    if( currentMillis - previousMillis >= 50 ) 
    {
      //digitalWrite(22,1);  
      //digitalWrite(23,0);
      previousMillis = currentMillis ;
      //analogWrite(3,55);  
        if(PID_L1.Compute()&&PID_L2.Compute()&&PID_R2.Compute()&&PID_R1.Compute()) //if( PID_L2.Compute() ) if ( PID_R2.Compute()) if( PID_R1.Compute()){
        {
           // S//erial.println("PWML1") ;
            //Serial.println(PWML1) ;
            switch(mode){
                case 0:
                    STOP(); break;
                case 1:
                    FORWARD();break;
                case 2:
                    BACK();;break;
                case 3:
                    LEFT();break;
                case 4:
                    RIGHT();break;
                case 5:
                    TURNLEFT();break;
                case 6:
                    TURNRIGHT();break;
                default :
                    STOP();break;
            }
             // 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT
            //10delay(10);
            //Serial.println("speedL1") ;            
            //Serial.println(speedL1) ;
            speedL1 = 0; speedL2 = 0; speedR1 = 0; speedR2 = 0;
        }      
        
    }
  }

/*
    //test
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
*/
}

//void Speed

void ReadMessage()
{

      
      delay(10);
      numdata = Serial.readBytes(serialData,9);  
      Serial.println("Serial.readBytes:");  
     TargetSpeed = 0;

     if((serialData[0]-'0')>=0&&(serialData[0]-'0')<=9) mode = serialData[0]-'0'; 
     if((serialData[2]-'0')>=0&&(serialData[2]-'0')<=9) TargetSpeed += (serialData[2]-'0') * 100;
     if((serialData[3]-'0')>=0&&(serialData[3]-'0')<=9) TargetSpeed += (serialData[3]-'0') * 10;
     if((serialData[4]-'0')>=0&&(serialData[4]-'0')<=9) TargetSpeed += (serialData[1]-'0') * 1;
      //第1位  模式（直走 倒退  左转 balabala
      //第3、4、5 位   目标速度
      //第7、8、9位  待定（可能是捡球机构、弹射机构的控制
      //Serial.println(speedL1);       //  
      //Serial.println(TargetSpeed);  
      //Serial.println(serialData); 
    while(Serial.read() >= 0){}  
    for(int i=0; i<18; i++)  serialData[i]='\0'; // clear serial buffer   
    
}


void TEST()
{
   // speed = map(speed,0,100,0,255);
   
    digitalWrite(22,1);    digitalWrite(26,0);
    digitalWrite(23,0);    digitalWrite(27,1);
    
    digitalWrite(24,1);    digitalWrite(28,0);
    digitalWrite(25,0);    digitalWrite(29,1);
    
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    delay(10);
}
void FORWARD()
{
   // speed = map(speed,0,100,0,255);
   
    digitalWrite(22,1);   digitalWrite(26,0);
    digitalWrite(23,0);   digitalWrite(27,1);
    
    digitalWrite(24,1);   digitalWrite(28,0); 
    digitalWrite(25,0);   digitalWrite(29,1);
     
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
   // delay(10);
}
void STOP()
{
    digitalWrite(22,0);   digitalWrite(26,0);
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,0);
    digitalWrite(25,0);   digitalWrite(29,0);
      
      
      
    //delay(10);
    
}
void BACK()
{
    //speed = map(speed,0,100,0,255)
    digitalWrite(22,0);   digitalWrite(26,1);
    digitalWrite(23,1);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,1);
    digitalWrite(25,1);   digitalWrite(29,0);
  
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    //delay(10);
}
void LEFT()
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,0);   digitalWrite(26,0); 
    digitalWrite(23,1);   digitalWrite(27,1);
    
    digitalWrite(24,1);   digitalWrite(28,1); 
    digitalWrite(25,0);   digitalWrite(29,0);
     
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    //delay(5);
}
void RIGHT()
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,1);   digitalWrite(26,1); 
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,0);   digitalWrite(28,0);  
    digitalWrite(25,1);   digitalWrite(29,1);
    
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    //delay(10);
}
void TURNLEFT()
{
   // speed = map(speed,0,100,0,255);
    digitalWrite(22,0);   digitalWrite(26,0); 
    digitalWrite(23,1);   digitalWrite(27,1);
    
    digitalWrite(24,0);   digitalWrite(28,0); 
    digitalWrite(25,1);   digitalWrite(29,1);

    
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    //delay(10);
}
void TURNRIGHT()
{
    //speed = map(speed,0,100,0,255);
    digitalWrite(22,1);   digitalWrite(26,1);  
    digitalWrite(23,0);   digitalWrite(27,0);
    
    digitalWrite(24,1);   digitalWrite(28,1); 
    digitalWrite(25,0);   digitalWrite(29,0);
  
    
    analogWrite(MotorL1,PWML1);  
    analogWrite(MotorL2,PWML2);
    analogWrite(MotorR1,PWMR1);   
    analogWrite(MotorR2,PWMR2);
    //delay(10);
}
