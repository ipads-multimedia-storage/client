import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
sys.path.append(project_dir + '/ObjectDetectionService')
import cv2
import time
import Camera
import threading
from ObjectDetectionService.lib import *
import arm_controller as AC

size = (640, 480)

od_client = ObjectDetectionClient('localhost:30307')
# od_client = ObjectDetectionClient('202.120.40.8:30307')

t1 = 0
count = 0
start_count_t1 = True
img_xs = []
img_ys = []

def run(img):
    global count
    global start_count_t1, t1
    global img_xs, img_ys

    response = od_client.upload(img)

    if response:
        img, img_x, img_y, color_area_max, angle = response
        img_xs.append(img_x)
        img_ys.append(img_y)
        count += 1
        
        if start_count_t1:
            start_count_t1 = False
            t1 = time.time()

        if count == 5:
            start_count_t1 = True
            
            vx = (img_xs[4] - img_xs[0]) / (time.time() - t1)
            vy = (img_ys[4] - img_ys[0]) / (time.time() - t1)
            # vx = 0
            # vy = 0
            print("--------")
            print("0: x: {}, y: {}".format(img_xs[0], img_ys[0]))
            print("1: x: {}, y: {}".format(img_xs[1], img_ys[1]))
            print("2: x: {}, y: {}".format(img_xs[2], img_ys[2]))
            print("3: x: {}, y: {}".format(img_xs[3], img_ys[3]))
            print("4: x: {}, y: {}".format(img_xs[4], img_ys[4]))
            print("vx: {}, vy: {}, time: {}".format(round(vx, 2), round(vy, 2), round(time.time() - t1, 2)))
            print("--------")

            # XXX: interval may not be the same
            # img_x = (img_xs[1] + img_xs[4] + img_xs[2] + img_xs[3]) / 2 - img_xs[0]
            # img_y = (img_ys[1] + img_ys[4] + img_ys[2] + img_ys[3]) / 2 - img_ys[0]
            img_xs = []
            img_ys = []

            sleep_time = 1.2
            img_x += vx * sleep_time
            img_y += vy * sleep_time

            AC.move(img_x, img_y, angle, needInfer=False)

            count = 0

    return img

if __name__ == '__main__':
    __target_color = ('red', 'green', 'blue')
    my_camera = Camera.Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame = run(frame)        
            cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()
