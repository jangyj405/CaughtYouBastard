import sys
sys.path.insert(1,'../model/')

from joolpr.infer import LPRModel
from joodetection.detector import get_detector

import cv2
import threading
import serial


block = 1

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
    import time
    time.sleep(10)
    ser.write(bytes(bytearray([100])))

def dummy_serial():
    while barrier_running:
        pass


def tcp_connection():
    print('tcp connected')

def free_tcp_socket():
    print('free tcp socket')

def dummy_tcp():
    while tcp_running:
        pass

def send_log_data(id:int, frame, block):
    print(f'send log to server : {id} {block} time:time!')


subjects = ['5721']
def compare_with_subjects(number : str):
    global subjects
    if number in subjects:
        return 1
    else:
        return 0
id = 0
barrier_thread = None
barrier_running = True
tcp_thread = None
tcp_running = True

serial_connection()
tcp_connection()

barrier_thread = threading.Thread(target=dummy_serial)
tcp_thread = threading.Thread(target=dummy_tcp)

barrier_thread.start()
tcp_thread.start()


sys.path.insert(1, '../model/joodetection/')
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
                send_log_data(id, frame, block)
                cv2.imshow("crop",cropped_frame)
            else:
                pass
    cv2.imshow('img', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
lpr_model.free()

## join barrier thread & release serial connection
if barrier_thread:
    barrier_running = False
    barrier_thread.join()
    free_serial()

## join tcp thread & release tcp socket
if tcp_thread:
    tcp_running = False
    tcp_thread.join()
    free_tcp_socket()
