#include <Servo.h>


Servo servo1;
Servo servo2;

void setup(){
  servo1.attach(3);
  servo2.attach(5);
  servo1.write(30);
  servo2.write(130);
  Serial.begin(9600);

}

void loop()
{
  if(Serial.available()){
    char ch = Serial.read();
    switch(ch){
      case 'd' :

        servo1.write(30);
        servo2.write(130);
        
        break;

      case 'u':
        servo1.write(120);
        servo2.write(30);
        
        break;
    }
  }
}