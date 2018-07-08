#include <PID_v1.h>

#include <Servo.h>

#define MotorL1 3

#define MotorL2 4 

#define MotorR1 5

#define MotorR2 6

int SpeedToPWM[256];

double speedL1,speedL2,speedR1,speedR2;

double PWML1,PWML2,PWMR1,PWMR2;

#define InterruptL1 5 //pin 18

#define InterruptL2 4 //pin 19

#define InterruptR1 3 //pin 20

#define InterruptR2 2 //pin 21

#define shoot 52

Servo ServoLeft;

Servo ServoRight;

#define up true

#define down false



bool pick = true;

int Steps = 0 ;

int StepsLeft = 13000 ;

bool Direction = 0 ; //0 -> down   1-> up



struct StepMotor

{

  int in1;

  int in2;

  int in3;

  int in4;

} StepM[2];



char serialData[18];  //储存信息

int numdata=0;

int mode;              // 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT

double TargetSpeed;



unsigned long previousMillis = 0 ;

unsigned long stepperMillis = 0 ;

unsigned long currentMillis = 0 ;

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

Serial.println("1") ;

    for(int i=22;i<=29;i++)        pinMode(i,OUTPUT);   //motor

    for(int i=32;i<=39;i++)        pinMode(i,OUTPUT);  //stepper

    for(int i=3;i<=6;i++)          pinMode(i,OUTPUT);  //motor

    pinMode(shoot,OUTPUT);

Serial.println("2") ;

    ServoLeft.attach(8);

    ServoRight.attach(9);

    StepM[0].in1 = 32; StepM[0].in2 = 33;

    StepM[0].in3 = 34; StepM[0].in4 = 35;

    StepM[1].in1 = 36; StepM[1].in2 = 37;

    StepM[1].in3 = 38; StepM[1].in4 = 39;

 Serial.println("3") ;   

    //TODO:   SERVO  degree

    ServoLeft.write(50);

    ServoRight.write(120);

    Direction = up;

//Serial.println("4") ;   

//    for(int i=1;i<=13000;i++)  //stepMotor   reset

//    {

//        stepper(0);

//        stepper(1);

//        delay(3);

//    }

//Serial.println("5") ;   

//     Direction = down;

//     for(int i=1;i<=10000;i++)  //stepMotor   reset

//     {

//         stepper(0);

//         stepper(1);

//         delay(2);

//     }



    attachInterrupt(InterruptL1 , ReadSpeedL1, CHANGE);attachInterrupt(InterruptR1 , ReadSpeedR1, CHANGE); attachInterrupt(InterruptL2 , ReadSpeedL2, CHANGE);attachInterrupt(InterruptR2 , ReadSpeedR2, CHANGE);



    PID_L1.SetMode(AUTOMATIC);PID_L1.SetSampleTime(50); PID_L2.SetMode(AUTOMATIC);PID_L2.SetSampleTime(50);PID_R1.SetMode(AUTOMATIC); PID_R1.SetSampleTime(50);PID_R2.SetMode(AUTOMATIC);//设置PID为自动模式 PID_R2.SetSampleTime(50);//设置PID采样频率为100ms

    // MsTimer2::set(100, Speed);        // 中断设置函数，每 100ms 进入一次中断

    // MsTimer2::start();                //开始计时

}



void loop()

{

    currentMillis = millis (); 

    if(Serial.available()>0)

    {  

      ReadMessage();

    }

    else

    {

      if( currentMillis - previousMillis >= 50 ) 

      {

        previousMillis = currentMillis ;

        if(PID_L1.Compute()&&PID_L2.Compute()&&PID_R2.Compute()&&PID_R1.Compute()) //if( PID_L2.Compute() ) if ( PID_R2.Compute()) if( PID_R1.Compute()){

        {

             // Serial.println("PWML1") ;

              //Serial.println(PWML1) ;

            switch(mode)

            {

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

                case 7:

                    PICK();break;

                case 8:

                    SHOOT();break;

                default :

                    STOP();break;

            }

             // 0->STOP  1->FORWARD  2->BACK   3->LEFT   4->RIGHT   5->TURNLEFT  6->TURNRIGHT

            speedL1 = 0; speedL2 = 0; speedR1 = 0; speedR2 = 0;

        }      

      }

    }

}



void stepper(int p){



  for (int x=0;x<1;x++){

    switch(Steps){

      case 0:

        digitalWrite(StepM[p].in1, LOW); 

        digitalWrite(StepM[p].in2, LOW);

        digitalWrite(StepM[p].in3, LOW);

        digitalWrite(StepM[p].in4, HIGH);

     break; 

     case 1:

        digitalWrite(StepM[p].in1, LOW); 

        digitalWrite(StepM[p].in2, LOW);

        digitalWrite(StepM[p].in3, HIGH);

        digitalWrite(StepM[p].in4, HIGH);

     break; 

     case 2:

        digitalWrite(StepM[p].in1, LOW); 

        digitalWrite(StepM[p].in2, LOW);

        digitalWrite(StepM[p].in3, HIGH);

        digitalWrite(StepM[p].in4, LOW);

    break; 

    case 3:

        digitalWrite(StepM[p].in1, LOW); 

        digitalWrite(StepM[p].in2, HIGH);

        digitalWrite(StepM[p].in3, HIGH);

        digitalWrite(StepM[p].in4, LOW);

    break; 

    case 4:

         digitalWrite(StepM[p].in1, LOW); 

         digitalWrite(StepM[p].in2, HIGH);

         digitalWrite(StepM[p].in3, LOW);

         digitalWrite(StepM[p].in4, LOW);

    break; 

    case 5:

         digitalWrite(StepM[p].in1, HIGH); 

         digitalWrite(StepM[p].in2, HIGH);

         digitalWrite(StepM[p].in3, LOW);

         digitalWrite(StepM[p].in4, LOW);

    break; 

    case 6:

         digitalWrite(StepM[p].in1, HIGH); 

         digitalWrite(StepM[p].in2, LOW);

         digitalWrite(StepM[p].in3, LOW);

         digitalWrite(StepM[p].in4, LOW);

     break; 

     case 7:

         digitalWrite(StepM[p].in1, HIGH); 

         digitalWrite(StepM[p].in2, LOW);

         digitalWrite(StepM[p].in3, LOW);

         digitalWrite(StepM[p].in4, HIGH);

     break; 

     default:

        digitalWrite(StepM[p].in1, LOW); 

        digitalWrite(StepM[p].in2, LOW);

        digitalWrite(StepM[p].in3, LOW);

        digitalWrite(StepM[p].in4, LOW);

      break; 

    }

    SetDirection();

  }

} 

void SetDirection(){

  if(Direction==1){ Steps++;}

  if(Direction==0){ Steps--; }

  if(Steps>7){Steps=0;}

  if(Steps<0){Steps=7;}

}

void PICK()

 {



    // myservo.write(120); // RIGHT   OPEN

    // myservo1.write(50);   //LEFT    

    // myservo.write(60);     //  close

    // myservo1.write(100); 

    Direction = down;



    for(int i=1;i<=4000;i++)  //stepMotor   down

    {

        stepper(0);

        stepper(1);

        delay(2);

    }



    TargetSpeed = 30 ;

    FORWARD();

    delay(400);

    for(int i =1;i<=200;i++)    //go & catch

    {

        FORWARD();

        ServoLeft.write(map(i,1,200,50,100));        //Catch

        ServoRight.write(map(i,1,200,120,60));

        delay(50);

    }



    delay(100);

    BACK();

    delay(100);

    STOP();

    delay(50);



    Direction = up;

    for(int i=1;i<=13000;i++)  //stepMotor   reset

    {

        stepper(0);

        stepper(1);

        delay(1);

    }

    FORWARD();

    delay(1000);



    mode = 0;

/*

    if( currentMillis - stepperMillis >= 1000 ) 

    {

        stepperMillis = currentMillis;

        if(StepsLeft > 0)

        {

            stepper(1);

            stepper(0);

            StepsLeft--;

        }

        if(StepsLeft == 0)

        {

            mode = 0 ;

            StepsLeft = 13000 ;

        }

    }

 }

*/

}

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

void SHOOT()

{

    digitalWrite(shoot,HIGH);

    delay(600);

    digitalWrite(shoot,LOW);

    delay(4);

    mode = 0 ;

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


