#!/usr/bin/python
import serial
import time
import threading
import sys
import defines


class SerialSetup(object):
    ser: serial.Serial()

    def __init__(self, ser):
        self.ser = ser
        # initialization and open the port
        self.set_default()

    # 获取串口实例
    def get_serial(self):
        return self.ser

    # 给前端显示可用的波特率数据
    def get_baudrate_list(self):
        return defines.baudrate_list

    # 设置端口
    def set_port(self, port: str):
        self.ser.port = port

    # 设置波特率
    def set_baudrate(self, baudrate: int = None):
        if baudrate in defines.baudrate_list:
            self.ser.baudrate = baudrate
            return True
        else:
            return False

    # 设置写延迟
    def set_write_timeout(self, write_timeout):
        if write_timeout > 10:
            self.ser.writeTimeout(write_timeout)
            return True
        else:
            return False

    # 设置读延迟
    def set_read_timeout(self, read_timeout):
        if read_timeout > 10:
            self.ser.timeout = read_timeout
            return True
        else:
            return False

    # 设置各个参数为默认值
    def set_default(self):
        # self.set_port("/dev/ttyAMA0")
        # ser.port = "/dev/ttyUSB0"
        # ser.port = "/dev/ttyS2"
        self.set_baudrate(9600)
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        # ser.timeout = None          # block read
        self.ser.timeout = 1  # non-block read
        # ser.timeout = 2              # timeout block read
        self.ser.xonxoff = False  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2  # timeout for write
        # possible timeout values:
        #    1. None: wait forever, block call
        #    2. 0: non-blocking mode, return immediately
        #    3. x, x is bigger than 0, float allowed, timeout block call


class SerialData(object):
    serial_virtual_device = {}

    def __init__(self):
        # self.set_active_virtual_device('device_1')  # todo: 用数据库读取来获取该值
        pass

    # 设置默认的模拟设备，如果设置成功返回True，设置不成功返回False
    def set_active_virtual_device(self, device_name):
        if device_name in self.serial_virtual_device:
            self.serial_virtual_device[defines.ACTIVE_DEVICE] = device_name
            return True
        else:
            return False

    def get_active_virtual_device(self):
        return self.serial_virtual_device[defines.ACTIVE_DEVICE]

    # 给指定的device_name的模拟设备添加单个输入输出数据，如果都正常返回True
    def add_virtual_device_data(self, device_name, receive_data, send_data):
        # 输入和输出数据进行确认，如果不是ascii字符则报错(串口只能使用ascii字符和数字)
        if type(receive_data) != int:
            try:
                receive_data.decode('ascii')
            except UnicodeDecodeError:
                return False
        if type(send_data) != int:
            try:
                send_data.decode('ascii')
            except UnicodeDecodeError:
                return False
        if device_name in self.serial_virtual_device:
            self.serial_virtual_device[device_name][receive_data] = send_data
        else:
            self.serial_virtual_device[device_name] = {receive_data: send_data}
        return True

    # 给指定的device_name的模拟设备设置响应数据集，如果出错则返回False，如果都正常返回True
    def set_virtual_device(self, device_name, respond_setting: dict):
        result = True
        for k, v in respond_setting.items():
            result = result and self.add_virtual_device_data(device_name, k, v)
        return result

    # 根据receive_data和默认的设备名称，获取字典中对应的输出数据，返回一个元组，第一位是是否成功，第二位是对应数据
    def get_response_data(self, receive_data):
        active_device_name = self.get_active_virtual_device()
        if receive_data in self.serial_virtual_device[active_device_name]:
            return True, self.serial_virtual_device[active_device_name][receive_data]
        else:
            return False, receive_data


class ResponseRequests(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser

    # 读取串口接收到的数据，根据接收到的数据发送数据的主线程
    def run(self):
        serial_data = SerialData()
        try:
            self.ser.flushInput()  # flush input buffer, discarding all its contents
            self.ser.flushOutput()  # flush output buffer, aborting current output
            # and discard all that is in buffer

            time.sleep(0.5)  # give the serial port sometime to receive the data
            while True:
                read_data = self.ser.read(1)
                read_data += self.ser.read(self.ser.inWaiting())

                if read_data != str.encode('', 'ascii'):
                    response = serial_data.get_response_data(read_data)
                    if response[0]:
                        print("%s read: %s " % (time.strftime('%H-%M-%S', time.localtime(time.time())), read_data))
                        self.send_serial_data(response[1])
                    else:
                        print("请求数据不正确 %s " % (read_data,))

        except Exception as e1:
            print("通信错误: " + str(e1))

    # 发送数据，参数可以是string也可以是int
    def send_serial_data(self, send_data):
        if type(send_data) != int:
            self.ser.write(str.encode(send_data, 'ascii'))
            print("%s 发送: %s " % (time.strftime('%H-%M-%S', time.localtime(time.time())), str.encode('send_data', 'ascii')))
        else:
            self.ser.write(send_data)
            print("%s 发送: %s " % (time.strftime('%H-%M-%S', time.localtime(time.time())), send_data))


def main():
    ser = serial.Serial()
    serial_setup = SerialSetup(ser)
    serial_setup.set_port("COM7")

    serial_data = SerialData()

    # 初始化数据
    respond_data = {str.encode("M1\r\n", 'ascii'): str.encode("M1," + '%+08.3f' % 555.555, 'ascii')}
    serial_data.set_virtual_device("焦距测量", respond_data)
    serial_data.set_active_virtual_device("焦距测量")

    try:
        serial_setup.get_serial().open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

    if serial_setup.get_serial().isOpen():
        t = ResponseRequests(serial_setup.get_serial())
        # t = threading.Thread(target=ResponseRequests, name='SerialResponse', args=(ser,))
        t.start()

        print('目前线程数 %d ,名称分别为: %s' % (threading.active_count(), threading.enumerate()))

        print("--------------------------")

        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    else:
        print("cannot open serial port ")


if __name__ == "__main__":
    main()
