# -*- coding: utf-8 -*-
#实验效果：红外发射模块
import sys
import time
from pinpong.board import Board,IRRemote,Pin

Board("UNIHIKER").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("UNIHIKER","COM36").begin()  #windows下指定端口初始化
#Board("UNIHIKER","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("UNIHIKER","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

ir = IRRemote(Pin(Pin.P22))

while True:
    ir.send(0xfd807f) #VOL+
    time.sleep(0.5)
    ir.send(0xfd906f) #VOL-
    time.sleep(0.5)