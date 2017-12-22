# import RPi.GPIO as GPIO
import time
import sys
import threading
from . import defines
from enum import Enum
from .libs import GPIO


class IoType(Enum):
    input = 0
    output = 1


class EdgeType(Enum):
    raising = 0
    falling = 1


# 对io接口的输入输出类型进行设置，并将设置保存下来，在启动时读取设置
class IoSetup(object):
    # 定义一个静态自动来保存每个io口的配置信息
    io_type = dict(io0=IoType.input, io1=IoType.input, io2=IoType.input, io3=IoType.input,
                   io4=IoType.input, io5=IoType.input, io6=IoType.input, io7=IoType.input,
                   io8=IoType.input, io9=IoType.input, io10=IoType.input, io11=IoType.input,
                   io12=IoType.input, io13=IoType.input, io14=IoType.input, io15=IoType.input)

    def __init__(self):
        self.gpio = GPIO
        pass

    def set_gpio(self, my_gpio):
        self.gpio = my_gpio

    def get_gpio(self):
        return self.gpio

    def set_io_mode(self):
        self.gpio.setmode(self.gpio.BOARD)

    def set_io_type(self, io_type: IoType, io_number):
        if io_number in defines.io_defines:
            io = defines.io_defines.get(io_number)
            if io_type == IoType.input:
                self.gpio.setup(io, self.gpio.IN, pull_up_down=self.gpio.PUD_DOWN)
                self.io_type[io_number] = IoType.input

            elif io_type == IoType.output:
                self.gpio.setup(io, self.gpio.OUT)
                self.io_type[io_number] = IoType.output
            else:
                print("IO设置类型错误")
                return False, "IO设置类型错误"
            return True
        else:
            print("IO编号名错误")
            return False, "IO编号名错误"

    def set_io_list(self, io_type: IoType, io_list):
        for io_number in io_list:
            self.set_io_type(io_type, defines.io_defines.get(io_number))

    def get_io_type(self, io_type):
        result = []
        for io_name in self.io_type:
            if self.io_type.get(io_name) == io_type:
                result.append(io_name)
        return result

    def io_cleanup_setup(self, io_number=None):
        if io_number is None:
            self.gpio.cleanup()
        else:
            io = defines.io_defines.get(io_number)
            self.gpio.cleanup(io)

    def set_edge_callback(self, input_port, edge_type: EdgeType, function_name):
        # todo: 需要把function_name换成具体的Function
        if edge_type == EdgeType.raising:
            self.gpio.add_event_detect(input_port, self.gpio.RISING, callback=function_name)
        else:
            self.gpio.add_event_detect(input_port, self.gpio.RISING, callback=function_name)

    def load_settings(self, db_instance):
        # todo: 读取数据库数据并执行初始化设置
        pass


# 对io的输出电平进行设置，获取输入电平高低
class IoData(object):
    io_prev_output_status = dict()

    def __int__(self):
        pass

    # 根据level设置io_number的电平高低，返回一个元组，第一位是是否成功，第二位是说明
    def set_output_data(self, io_number, level: bool):
        iosetup = IoSetup()
        if io_number in defines.io_defines:
            if io_number in iosetup.get_io_type(IoType.output):
                iosetup.get_gpio().output(defines.io_defines.get(io_number), level)
                self.io_prev_output_status[io_number] = level
                result = (True, io_number)
            else:
                result = (False, io_number + "不是输出接口，无法设置")
        else:
            result = (False, io_number + "编号错误")
        return result

    # 对list中每个io根据level设置电平高低，返回结果列表，列表中每条内容是一个元组
    def set_outputs_data(self, io_list: list, level: bool):
        result = []
        for io_number in io_list:
            result.append(self.set_output_data(io_number, level))
        return result

    # 根据io_number获取接口的电平高低，返回一个元组如果成功元组第一位是io_number，第二位是电平值，
    # 如果不成功第一位是False，第二位是原因
    def get_data(self, io_number):
        iosetup = IoSetup()
        if io_number in defines.io_defines:
            if io_number in iosetup.get_io_type(IoType.input):
                io = defines.io_defines.get(io_number)
                result = (io_number, iosetup.get_gpio().input(io))
            else:
                if io_number in self.io_prev_output_status:
                    result = (io_number, self.io_prev_output_status[io_number])
                else:
                    result = (False, '输出接口' + io_number + "没有初始化")
        else:
            result = (False, io_number + "编号错误")
        return result

    def get_inputs_data(self, io_list):
        result = []
        for io_number in io_list:
            result.append(self.get_data(io_number))
        return result
