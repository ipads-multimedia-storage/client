import socket
import cv2
import numpy
import time
import sys
import json


def send_video():
    address = ('localhost', 8002)

    try:
        # socket.SOCK_STREAM：for TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("sending side: built connection with " + str(address))
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()   # ret == 1 for success, 0 for failure
    time_stamp = int(round(time.time() * 1000))  # record event time
    # jpeg, '95' for quality, higher the number, higher the quality(0-100)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

    while ret:
        # time.sleep(0.01)  # you can put it to sleep in each loop to release the pressure of server
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # built mat
        data = numpy.array(imgencode)
        string_data = data.tostring()
        # 'current_time': enable server to calculate bandwidth
        current_time = int(round(time.time() * 1000))
        body = {"length": len(string_data), "event_time": time_stamp, "current_time": current_time}
        body = json.dumps(body)
        sock.send(str.encode(str(len(body)).ljust(16)))
        sock.send(body.encode('utf-8'))
        sock.send(string_data)
        # then read next frame
        ret, frame = capture.read()
        time_stamp = int(round(time.time() * 1000))
        # if cv2.waitKey(10) == 27:
        #     break
    sock.close()

     
if __name__ == '__main__':
    send_video()
