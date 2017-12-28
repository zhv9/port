from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from ...hardware import serial_manager
from ...hardware import defines

app = Flask(__name__)
api = Api(app)


class SerialSetting(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()

    def get(self):
        result = {
            'setting': {'service': {}},
            'device': {'active_device': {}}
        }
        result['setting']['service']['baudrate'] = self.my_serial.get_serial().baudrate
        result['setting']['service']['serial_port'] = self.my_serial.get_serial().port
        result['setting']['service']['read_timeout'] = self.my_serial.get_serial().timeout
        result['setting']['service']['write_timeout'] = self.my_serial.get_serial().write_timeout

        result['setting']['device']['active_device'] = self.my_device.get_active_virtual_device()
        result['setting']['device'] = self.my_device.get_virtual_device()

        return {'serial_setup': result}


class SerialSettingService(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('serial_service', type={}, help='串口设置', location='json')

    def get(self):
        result = {
            'setting': {'service': {}},
            'device': {'active_device': {}}
        }
        result['setting']['service']['baudrate'] = self.my_serial.get_serial().baudrate
        result['setting']['service']['serial_port'] = self.my_serial.get_serial().port
        result['setting']['service']['read_timeout'] = self.my_serial.get_serial().timeout
        result['setting']['service']['write_timeout'] = self.my_serial.get_serial().write_timeout
        return {'serial_setup': result}

    def post(self):
        self.put()

    def put(self):
        result = []
        args = self.parser.parse_args()
        if 'baudrate' in args.keys():
            result.append(self.my_serial.set_baudrate(args['baudrate']))
        if 'serial_port' in args.keys():
            result.append(self.my_serial.set_baudrate(args['serial_port']))
        if 'read_timeout' in args.keys():
            result.append(self.my_serial.set_baudrate(args['read_timeout']))
        if 'write_timeout' in args.keys():
            result.append(self.my_serial.set_baudrate(args['write_timeout']))

        return {'serial_setup_result', result}


class SerialSettingDevice(Resource):
    def __init__(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_device = serial_manager.SerialData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('serial_device', type=[], help='串口设置', location='json')

    def get(self):
        result = self.my_device.get_virtual_device()
        # result['active_device'] = self.my_device.get_active_virtual_device()

        return {'device': result}

    # 添加虚拟设备
    def post(self):
        args = self.parser.parse_args()
        result = bool
        for device_name, respond_setting in args.items():
            result = self.my_device.set_virtual_device(device_name, respond_setting)

        if result is False:
            abort(500)
        else:
            return '', 200

    def put(self):
        self.post()

    def delete(self, device_name):
        result = self.my_device.delete_virtual_device(device_name)
        if result:
            return '', 200
        else:
            return '', 500


class SerialSettingActiveDevice(Resource):
    def __init__(self):
        self.my_device = serial_manager.SerialData()

    def get(self):
        result = self.my_device.get_active_virtual_device()
        return {'active_device': result}

    def post(self, device_name):
        self.put(device_name)

    def put(self, device_name):
        result = self.my_device.set_active_virtual_device(device_name)
        if result:
            return '', 200
        else:
            return '', 500


api.add_resource(SerialSetting, '/api/serial/setting/service/')
api.add_resource(SerialSettingService, '/api/serial/setting/service/')
api.add_resource(SerialSettingDevice, '/api/serial/setting/device/<device_name>')
api.add_resource(SerialSettingActiveDevice, '/api/serial/setting/device/active_device/<device_name>')

if __name__ == '__main__':
    app.run(debug=True)
