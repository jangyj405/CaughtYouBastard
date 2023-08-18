#include <Servo.h>


Servo servo1;
Servo servo2;

void setup(){
  servo1.attach(3);
  servo2.attach(5);
  servo1.write(90);
  servo2.write(0);
  Serial.begin(9600);

}

void loop()
{
  if(Serial.available()){
    char ch = Serial.read();
    switch(ch){
      case 'u' :

        servo1.write(0);
        servo2.write(90);
        
        break;

      case 'd':
        servo1.write(90);
        servo2.write(0);
        
        break;
    }
  }
}