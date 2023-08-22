import sys
sys.path.insert(1,'../model/')
sys.path.insert(1, '../model/joodetection/')
import threading
import time
import base64

import cv2
import serial

from joolpr.infer import LPRModel
from joodetection.detector import get_detector
from tcp_function import *

ser = None
def free_serial():
    global ser
    if ser:
        ser.close()
    print('free serial')

def serial_connection():
    global ser
    ser = serial.Serial('/dev/ttyACM0')
    print('serial connected')

def activate_barrier():
    global ser
    ser.write(bytes(bytearray([117])))
    print('barrier activate')
    thread = threading.Thread(target=deactivate_barrier)
    thread.start()

def deactivate_barrier():
    global ser
    time.sleep(10)
    ser.write(bytes(bytearray([100])))

subjects = []
polling_running = True
polling_thread = None
def polling_subject_number():
    global polling_running
    global subjects
    while polling_running:
        try:
            str_list = get_car_num_list()
            subjects = [s.strip() for s in str_list.replace('[','').replace(']','').replace('\n', '').replace('\"','').split(',')]
            time.sleep(1)
        except:
            pass
polling_thread = threading.Thread(target=polling_subject_number)
polling_thread.start()
def compare_with_subjects(number : str):
    global subjects
    if number in subjects:
        return 1
    else:
        return 0
data_buffer = []
tcp_running = True
def send_data_subroutine():
    global data_buffer
    global tcp_client
    while tcp_running:
        if len(data_buffer) > 0:
            try:
                id, frame, number = data_buffer.pop()
                send_log_data(tcp_client, id, frame, number)
            except:
                pass
            finally:
                data_buffer.clear()
            pass
        else:
            time.sleep(0.1)
            pass

id = 0

serial_connection()
tcp_client = tcp_connection()

tcp_thread = threading.Thread(target=send_data_subroutine)
tcp_thread.start()

detector = get_detector()
lpr_model = LPRModel()
cap = cv2.VideoCapture(2)
while 1:
    ret, frame = cap.read()
    if not ret:
        break
    cropped = detector.infer(frame)
    for crop in cropped:
        cropped_frame, tl, br = crop
        x,y = tl
        if not y > 180:
            continue
        number, output = lpr_model.infer(cropped_frame)
        if len(number) == 4:
            is_subject = compare_with_subjects(number)
            if is_subject:
                cv2.rectangle(frame, tl, br, (0,0,255), thickness=3)
                activate_barrier()
                success, buffer = cv2.imencode('.jpg', frame)
                if success:
                    print(type(buffer))
                    encoded_img = base64.b64encode(buffer).decode(encoding='utf-8')
                    data_buffer.append((id, encoded_img, number))
                cv2.imshow("crop",cropped_frame)
            else:
                pass
    cv2.imshow('img', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

#free resources
cap.release()
cv2.destroyAllWindows()
lpr_model.free()
free_serial()
free_tcp_sosket(tcp_client)
tcp_running = False
tcp_thread.join()
polling_running = False
polling_thread.join()
