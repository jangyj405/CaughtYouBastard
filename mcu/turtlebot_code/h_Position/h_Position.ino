#include <DynamixelWorkbench.h>

#define BAUDRATE            57600
#define BAUDRATE_TO_DXL     1000000
#define LEFT_ID             1
#define RIGHT_ID            2
 
DynamixelWorkbench dxl_wb;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(BAUDRATE);
    while (!Serial); // Open a Serial Monitor

    dxl_wb.begin("", BAUDRATE_TO_DXL);
    dxl_wb.ping(LEFT_ID);
    dxl_wb.ping(RIGHT_ID);

    dxl_wb.jointMode(LEFT_ID);
    dxl_wb.jointMode(RIGHT_ID);
}

void loop() {
    // put your main code here, to run repeatedly:
    //clockwise rotation
    dxl_wb.wheelMode(1);
    dxl_wb.wheelMode(2);

    // 회전 속도 설정 (값은 모터에 따라 다름)
    dxl_wb.goalVelocity(1, -100);  // 양수: 시계방향, 음수: 반시계방향
    dxl_wb.goalVelocity(2, -100);  // -값 전진  +값 후진

    // 일정 시간 동안 회전을 유지
    delay(100000); // 100초간 전진

    // 회전 중지
    //dxl_wb.goalVelocity(MOTOR_ID, 0);