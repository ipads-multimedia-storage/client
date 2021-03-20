from xmlrpc.server import SimpleXMLRPCServer
import random
import binascii
import serial  
import time
import sys
# import numpy as np


# the command of the switch of the conveyor
# switch on
# FE 05 00 00 FF 00 98 35
# FE 05 00 01 FF 00 C9 F5
# switch off
# FE 05 00 00 00 00 D9 C5
# FE 05 00 01 00 00 88 05

class CenterControlService:
    def __init__(self, car_number, arm_number, mode=1):
        print("server starts")
        # car postion status: arm2, arm3, move
        self.car_pos = []
        for i in range(car_number):
            self.car_pos.append('arm2')

        # arm status: wait, ready, startPick, pickEnd, putEnd, finish
        self.arm_status = []
        for i in range(arm_number):
            self.arm_status.append('wait')

        # the serialPort
        # TODO: my com id
        self.serialPort = serial.Serial("com3", 9600)  

        # conveyor status: run, stop
        self.conveyor_status = 'run'
        if mode == 1:
            self.ConveyorSwitch('run')
        else:
            self.ConveyorSwitch('stop')

        # self.f = open("log.txt", "a")

        self.block_color = []
        for i in range(arm_number):
            self.block_color.append('None')               
    
    def ConveyorSwitch(self, cmd):
        # print("change conveyor status: %s", cmd)
        strOn  = 'FE 05 00 01 FF 00 C9 F5'
        strOff = 'FE 05 00 01 00 00 88 05'
        if cmd == 'run':
            try:
                self.serialPort.write(bytes.fromhex(strOn))
            except:
                n = self.serialPort.write(bytes(strOn,encoding='utf-8'))
                print('switch on fail', n)
        elif cmd == 'stop':
            try:
                self.serialPort.write(bytes.fromhex(strOff))
            except:
                n = self.serialPort.write(bytes(strOff,encoding='utf-8'))
                print('switch off fail', n)


    def get_color_status(self, arm_id, car_id = None):
        print("get_arm_status, arm_id", arm_id)
        return self.block_color[arm_id]
    
    def set_color_status(self, arm_id, status):
        print("get_arm_status, arm_id", arm_id)
        self.block_color[arm_id] = status

    def get_car_postion(self, car_id, arm_id = None):
        print("get_car_postion, arm_id", arm_id, "car_id", car_id)
        return self.car_pos[car_id]

    def set_car_postion(self, car_id, pos):
        print("set_car_postion, car_id", car_id, "pos", pos)
        self.car_pos[car_id] = pos

    def get_arm_status(self, arm_id, car_id = None):
        print("get_arm_status, arm_id", arm_id)
        return self.arm_status[arm_id]
    
    def get_set_arm_status_not(self, arm_id, not_status, status):
        print("get_arm_status, arm_id", arm_id)
        if self.arm_status[arm_id] != not_status:
            self.arm_status[arm_id] = status
            return True
        else:
            return False

    def get_set_arm_status_is(self, arm_id, is_status, status):
        print("get_arm_status, arm_id", arm_id)
        if self.arm_status[arm_id] == is_status:
            self.arm_status[arm_id] = status
            return True
        else:
            return False
    
    def set_arm_status(self, arm_id, status, source = None):
        print("set_arm_status, arm_id", arm_id, "status", status)
        # self.f.write("set_arm_status, arm_id，" +str(arm_id) +", status, "+str(status)+ ", source, " +str(source)+ "\n")
        self.arm_status[arm_id] = status

    def set_conveyor_status(self, status):
        print("set_conveyor_status", status)
        self.ConveyorSwitch(status)
        self.conveyor_status = status

    def get_conveyor_status(self):
        print("get_conveyor_status", self.conveyor_status)
        return self.conveyor_status


def main():
    mode = int(sys.argv[1])
    service = CenterControlService(2, 3, mode)
    server = SimpleXMLRPCServer(('0.0.0.0', 50051), allow_none=True)
    server.register_instance(service)
    server.serve_forever()


if __name__ == '__main__':
    main()
