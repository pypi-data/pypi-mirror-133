# -*- coding: utf-8 -*-

#实验效果：打印PythonBoard板所有模拟口的值
#接线：使用windows或linux电脑连接一块arduino主控板，主控板A0接一个模拟传感器
import time
from pinpong.board import Board,Pin,ADC  #导入ADC类实现模拟输入

Board("UNIHIKER").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("UNIHIKER","COM36").begin()   #windows下指定端口初始化
#Board("UNIHIKER","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("UNIHIKER","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

#P0 P1 P3 P4 P10 P21 P22
adc0 = ADC(Pin(Pin.P0)) #将Pin传入ADC中实现模拟输入
adc1 = ADC(Pin(Pin.P1))
adc3 = ADC(Pin(Pin.P3))
adc4 = ADC(Pin(Pin.P4))
adc10 = ADC(Pin(Pin.P10))
adc21 = ADC(Pin(Pin.P21))
adc22 = ADC(Pin(Pin.P22))

while True:
  print("P0=", adc0.read())
  print("P1=", adc1.read())
  print("P3=", adc3.read())
  print("P4=", adc4.read())
  print("P10=", adc10.read())
  print("P21=", adc21.read())
  print("P22=", adc22.read())
  print("------------------")
  time.sleep(0.5)
