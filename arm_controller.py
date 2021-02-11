import sys
import os
import time
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board

AK = ArmIK()

# turn on the light to red
def set_light():
    Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
    Board.RGB.show()

# turn off the light
def reset_light():
    Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
    Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
    Board.RGB.show()

# ring the buzzer for prompt
def set_buzzer(ring_time):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(ring_time)
    Board.setBuzzer(0)

def move_to_init_pos():
    Board.setBusServoPulse(1, 450, 300)
    rotater_reset()
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

# make the arm move to specified position
# return value: time spent
def move_to_pos(x, y, z):
    result = AK.setPitchRangeMoving((x, y, z), -90, -90, 0)
    if result == False:
        return False
    
    # result[2] is the time spent to move to that position
    return result

# servo 1 (aka. gripper) is responsible to grab the object
def gripper_tighten():
    Board.setBusServoPulse(1, 500, 500)

def gripper_loose():
    Board.setBusServoPulse(1, 220, 500)

# servo 2 (aka. rotater) is responsible to rotate the gripper
def rotater_set_to(angle):
    Board.setBusServoPulse(2, angle, 500)

def rotater_reset():
    rotater_set_to(500)


def convertByTimeInterval(image_x, image_y, speed, event_time):
    # XXX: where to get the direction of speed
    # assume it's along +x direction
    current_time = round(time.time() * 1000)
    # sleep time is 2.1s
    sleep_time = 2100
    # assume 200ms deviation
    episilon = 200

    delta_time = current_time + sleep_time + episilon - event_time
    image_x += delta_time * speed
    return image_x, image_y
    
def move(image_x, image_y, angle, speed, event_time):
    # convert image coord to world coord
    image_x, image_y = convertByTimeInterval(image_x, image_y, speed, event_time)
    world_x, world_y = convertCoordinate(image_x, image_y)

    # set light and buzzer just for a prompt
    set_light()
    set_buzzer(0.1)
    
    result = move_to_pos(world_x, world_y, 7)
    if result == False:
        print("cannot move to specified position")
        return False

    rotater_angle = getAngle(world_x, world_y, angle)
    gripper_loose()
    rotater_set_to(rotater_angle)
    time.sleep(0.5)
    
    move_to_pos(world_x, world_y, 1.5)
    time.sleep(1.5)

    # at this point, gripper should arrive at the catching position
    # so the total sleep time is 2.1s

    gripper_tighten()
    # if not perform well, 
    # we could lower the sleep time here to let gripper catch more quickly
    time.sleep(0.8)

    rotater_reset()
    move_to_pos(world_x, world_y, 12)
    time.sleep(1)

    coord_to_put = (-14.5, 11.5)

    result = move_to_pos(coord_to_put[0], coord_to_put[1], 12)
    assert result != False
    time.sleep(result[2] / 1000)
    
    rotater_angle = getAngle(coord_to_put[0], coord_to_put[1], -90)
    rotater_set_to(rotater_angle)
    time.sleep(0.5)

    result = move_to_pos(coord_to_put[0], coord_to_put[1], 4.5)
    time.sleep(0.5)
    
    result = move_to_pos(coord_to_put[0], coord_to_put[1], 1.5)
    time.sleep(0.8)

    gripper_loose()
    time.sleep(0.8)

    result = move_to_pos(coord_to_put[0], coord_to_put[1], 12)
    time.sleep(0.8)

    move_to_init_pos()
    time.sleep(1.5)

    reset_light()
    