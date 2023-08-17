#include <NewPing.h>
#include <DynamixelWorkbench.h>

#define BAUDRATE            57600
#define BAUDRATE_TO_DXL     1000000
#define LEFT_ID             1
#define RIGHT_ID            2
#define MAX_DISTANCE  200

DynamixelWorkbench dxl_wb;

NewPing sonar(BDPIN_GPIO_1, BDPIN_GPIO_2, MAX_DISTANCE);
const int trigPin = BDPIN_GPIO_1;
const int echoPin = BDPIN_GPIO_2;

float duration, distance;
void setup() {

  //Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
    // put your setup code here, to run once:
    Serial.begin(BAUDRATE);
    //while (!Serial); // Open a Serial Monitor

    dxl_wb.begin("", BAUDRATE_TO_DXL);
    dxl_wb.ping(LEFT_ID);
    dxl_wb.ping(RIGHT_ID);

    dxl_wb.jointMode(LEFT_ID);
    dxl_wb.jointMode(RIGHT_ID);
    dxl_wb.wheelMode(1);
    dxl_wb.wheelMode(2);
}
unsigned long sensor_elapsed_time = 0;
unsigned long trig_elapsed_time = 0;
unsigned char sensorflag = 0;
double sumDistance = 0;
double avgDistance = 0;
unsigned char sumcnt = 0;

void loop() {
    // put your main code here, to run repeatedly:
    //clockwise rotation
  if(sensorflag == 0)
  {
    sensor_elapsed_time = millis();
    sumDistance = 0;
    sensorflag=1;
  }

  else if(sensorflag == 1)
  {
    if((millis() - sensor_elapsed_time) > 20)
    { 
      digitalWrite(trigPin, HIGH);
      delay(10);     
      digitalWrite(trigPin, LOW);
      
      
  
      duration = pulseIn(echoPin, HIGH);
      distance = ((float)(340 * duration) / 10000) / 2;
      sumDistance = sumDistance + distance;
      //Serial.print(" sumDistance: ");
      //Serial.print(sumDistance);
      //Serial.print(" elapsed time: ");
      //Serial.println(sensor_elapsed_time);
      
      sumcnt++;
      sensor_elapsed_time = millis();
      
      if(sumcnt > 4)
      {
        sensorflag = 0;
        avgDistance = sumDistance / 5.0;
        sumcnt = 0;
        //Serial.print(" avgDistance: ");
        //Serial.println(avgDistance);
      }
    }
  }

  Serial.print(" motor_avgDistance: ");
  Serial.println(avgDistance);
  if(avgDistance < 10)
  {
    dxl_wb.goalVelocity(1, 0);
    dxl_wb.goalVelocity(2, 0);  
  }

  else 
  {
    dxl_wb.goalVelocity(1, -100);  // 양수: 시계방향, 음수: 반시계방향
    dxl_wb.goalVelocity(2, -100);  // -값 전진  +값 후진
  }
    
}