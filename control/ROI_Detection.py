import sys
sys.path.insert(1,'../model/')
from joolpr.infer import LPRModel
import cv2
import numpy as np
import base64
import threading
from tcp_function import tcp_connection, send_log_data, free_tcp_sosket, get_car_num_list

subjects =  get_car_num_list()
print("car Num List is ", subjects)

cleint_socket = tcp_connection()


# Replace '/dev/ttyACM0' with the correct port
# arduino = Serial('/dev/ttyACM0', 9600)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

lpr_model = LPRModel()

while True:
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = 0 if h == 0 else float(w) / h

                area = w * h
                if 7500 < area < 9500 and 2.3 <= aspect_ratio <= 2.7:
                    boxed_part = img[y:y + h, x:x + w]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.imshow('Boxed Part', boxed_part)
                    number, output_img = lpr_model.infer(boxed_part)
                    print(number)
                    if len(number) == 4:

                        success, buffer = cv2.imencode('.jpg', img)#cv2.imread("./result2.png")#

                        if success:
                            print(type(buffer))
                            encoded_img = base64.b64encode(buffer).decode(encoding='utf-8')
                            print(encoded_img)
                            #json_byte = get_json_byte(encoded_img.decode(), number)

                            #print(encoded_img)
                            #send_log_data(cleint_socket, '0', encoded_img, number)
                            print("t1")
                            t1 = threading.Thread(target=send_log_data, args=[cleint_socket,'0', encoded_img, number])
                            t1.start()
                            #cleint_socket.sendall(bytes(json_byte, encoding='utf-8'))
                            #time.sleep(12)

                    # client_socket.sendall(b'1')

                    last_x, last_y, last_w, last_h = x, y, w, h

    cv2.imshow("Detected Objects", img)
    cv2.imwrite('result.png', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        final_img = img
        final_box = (last_x, last_y, last_w, last_h)
        t1.join()
        break
lpr_model.free()
cap.release()
cv2.destroyAllWindows()
