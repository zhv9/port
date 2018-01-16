# import sys
# sys.path.append('../..')
import json
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
from src.hardware import serial_manager
from src.hardware import defines


class SerialSetting(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()

    def get(self):
        result = {
            'setting': {'service': {},
                        'device': {'active_device': str}
                        }
        }
        result['setting']['service']['baudrate'] = self.my_serial.get_serial().baudrate
        result['setting']['service']['serial_port'] = self.my_serial.get_serial().port
        result['setting']['service']['read_timeout'] = self.my_serial.get_serial().timeout
        result['setting']['service']['write_timeout'] = self.my_serial.get_serial().write_timeout
        result['setting']['device'] = self.my_device.get_virtual_device()
        result['setting']['device']['active_device'] = self.my_device.get_active_virtual_device()

        return {'serial_setup': result}


class SerialSettingService(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('serial_service')

    def get(self):
        result = {
            'service': {},
        }
        result['service']['baudrate'] = self.my_serial.get_serial().baudrate
        result['service']['serial_port'] = self.my_serial.get_serial().port
        result['service']['read_timeout'] = self.my_serial.get_serial().timeout
        result['service']['write_timeout'] = self.my_serial.get_serial().write_timeout
        return {'serial_service_setting': result}

    def post(self):
        return self.put()

    def put(self):
        result = []
        args = request.get_json()
        if 'baudrate' in args.keys():
            result.append(self.my_serial.set_baudrate(args['baudrate']))
        if 'serial_port' in args.keys():
            result.append(self.my_serial.set_port(args['serial_port']))
        if 'read_timeout' in args.keys():
            result.append(self.my_serial.set_read_timeout(args['read_timeout']))
        if 'write_timeout' in args.keys():
            result.append(self.my_serial.set_write_timeout(args['write_timeout']))

        return {'serial_setup_result': result}


class SerialSettingDevices(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('serial_device', help='串口数据设置', location='json')

    def get(self):
        result = {}
        result = self.my_device.get_virtual_device()
        # result['active_device'] = self.my_device.get_active_virtual_device()
        return {'serial_device': result}

    # 添加虚拟设备
    def post(self):
        args = request.get_json()
        result = {}
        if defines.ACTIVE_DEVICE in args['serial_device']:
            args['serial_device'].pop(defines.ACTIVE_DEVICE)
        for device, respond_setting in args['serial_device'].items():
            result[device] = self.my_device.set_virtual_device(device, respond_setting)
        return result

    def put(self):
        return self.post()


class SerialSettingDevice(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('serial_device', help='串口数据设置', location='json')

    def get(self, device_name):
        result = self.my_device.get_virtual_device()
        if device_name is not None:
            if device_name in result:
                result = {device_name: result[device_name]}
            else:
                abort(404)
        return {'serial_device': result}

    # 添加虚拟设备
    def post(self, device_name):
        args = request.get_json()
        result = {}
        for value in args[device_name]:
            result[device_name] = self.my_device.add_virtual_device_data(device_name, value.get('receive', value.get('send')))
        return result

    def put(self, device_name):
        return self.post(device_name)

    def delete(self, device_name):
        result = self.my_device.delete_virtual_device(device_name)
        return {device_name: result}


class SerialSettingActiveDevice(Resource):
    def __init__(self):
        self.my_device = serial_manager.SerialData()

    def post(self, device_name):
        return self.put(device_name)

    def put(self, device_name):
        result = self.my_device.set_active_virtual_device(device_name)
        return {device_name: result}


class SerialSettingActiveDeviceGet(Resource):
    def __init__(self):
        self.my_device = serial_manager.SerialData()

    def get(self):
        result = self.my_device.get_active_virtual_device()
        return {'active_device': result}


def init_api(api):
    api.add_resource(SerialSetting, '/api/serial/setting/')
    api.add_resource(SerialSettingService, '/api/serial/setting/service/')
    api.add_resource(SerialSettingDevices, '/api/serial/setting/device/', endpoint='devices')
    api.add_resource(SerialSettingDevice, '/api/serial/setting/device/<string:device_name>', endpoint='device')
    api.add_resource(SerialSettingActiveDeviceGet, '/api/serial/setting/device/active_device/')
    api.add_resource(SerialSettingActiveDevice, '/api/serial/setting/device/active_device/<device_name>')


if __name__ == '__main__':
    app = Flask(__name__,
                static_folder="../static",
                template_folder="../templates")
    my_api = Api(app)
    init_api(my_api)
    app.run(debug=True)
