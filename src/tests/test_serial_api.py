import unittest
import json
from unittest import mock
from unittest.mock import patch
from src.app.api import serial_api
from flask_restful import Api
from flask import Flask
from src.hardware import serial_manager
from src.hardware import defines

from src.tests import util


class TestSerialSetting(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.my_serial_setting = serial_manager.SerialSetup()
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        self.my_serial_data.serial_virtual_device.clear()

    # @patch.object(serial_manager.SerialData, 'get_virtual_device')
    def test_get(self):
        # util = SerialTestUtil()
        # util.add_virtual_device(self.my_serial_data)
        # util.set_virtual_device(self.my_serial_data)
        # mock_get_virtual_device.return_value = SerialTestUtil.data
        self.my_serial_setting.set_baudrate(38400)

        send_data = {
            '测试1': [
                {'receive': 'receive1\r\n', 'send': 'send1\r\n'},
                {'receive': 'receive2\r\n', 'send': 'send2\r\n'},
                {'receive': 'receive3\r\n', 'send': 'send3\r\n'},
                {'receive': 'receive4\r\n', 'send': 'send4\r\n'},
            ],
            '测试2': [
                {'receive': 'receiveA\r\n', 'send': 'sendA\r\n'},
                {'receive': 'receiveB\r\n', 'send': 'sendB\r\n'},
                {'receive': 'receiveC\r\n', 'send': 'sendC\r\n'},
            ]
        }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)
        self.client.post('/api/serial/setting/device/active_device/' + '测试1', headers=util.headers)
        expected = {"serial_setup": {"setting": {
            "service": {"baudrate": 38400, "serial_port": None, "read_timeout": None, "write_timeout": None},
            "device": self.my_serial_data.serial_virtual_device}}}
        result = self.client.get('/api/serial/setting/')
        self.assertEqual(200, result.status_code)
        self.assertEqual(expected, json.loads(result.data))


class TestSerialSettingService(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        self.my_serial_data.serial_virtual_device.clear()

    def test_put__use_correct_data__return_200(self):
        send_data = {'baudrate': 115200, 'serial_port': 'com1', 'read_timeout': 2000, 'write_timeout': 3000}
        response = self.client.put('/api/serial/setting/service/', headers=util.headers, data=json.dumps(send_data))
        self.assertEqual(200, response.status_code)
        self.assertEqual([True, None, True, True], json.loads(response.data)['serial_setup_result'])

    def test_put__use_error_data__return_False(self):
        send_data = {'baudrate': 5, 'serial_port': 'com1', 'read_timeout': 10}
        response = self.client.put('/api/serial/setting/service/', headers=util.headers, data=json.dumps(send_data))
        self.assertEqual(200, response.status_code)
        self.assertEqual([False, None, False], json.loads(response.data)['serial_setup_result'])

    def test_post(self):
        send_data = {'baudrate': 115200, 'serial_port': 'com1'}
        response = self.client.post('/api/serial/setting/service/', headers=util.headers, data=json.dumps(send_data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, json.loads(response.data)['serial_setup_result'][0])

    def test_get(self):
        send_data = {'baudrate': 115200, 'serial_port': 'com1', 'read_timeout': 2000, 'write_timeout': 3000}
        self.client.post('/api/serial/setting/service/', headers=util.headers, data=json.dumps(send_data))
        response = self.client.get('/api/serial/setting/service/')
        receive_data = json.loads(response.data)['serial_service_setting']['service']
        self.assertEqual(200, response.status_code)
        self.assertEqual(send_data, receive_data)


class TestSerialSettingDevices(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.name = 'serial_device'
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        self.my_serial_data.serial_virtual_device.clear()

    def test_post__ok_data__return_true(self):
        send_data = {
            '测试1': [
                {defines.RECEIVE_DATA: 'receive1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: 'receive4\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: 'sendA\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: 'sendC\r\n'},
            ]
        }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        response = self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        expected = {'测试1': [True, True, True, True], '测试2': [True, True, True]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, json.loads(response.data))

    def test_post__have_active_device_data__return_true(self):
        send_data = {
            'active_device': '测试1',
            '测试1': [
                {defines.RECEIVE_DATA: 'receive1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: 'receive4\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: 'sendA\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: 'sendC\r\n'},
            ]
        }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        response = self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        expected = {'测试1': [True, True, True, True], '测试2': [True, True, True]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, json.loads(response.data))

    def test_post__utf8_data__return_false(self):
        send_data = {
            '测试1': [
                {defines.RECEIVE_DATA: '错误数据1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: '错误数据2\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: '错误返回值\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: '错误返回值\r\n'},
            ]
        }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        response = self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        excepted = {'测试1': [False, True, True, False], '测试2': [False, True, False]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(excepted, json.loads(response.data))

    def test_get(self):
        send_data = {
            '测试1': [
                {defines.RECEIVE_DATA: 'receive1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: 'receive4\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: 'sendA\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: 'sendC\r\n'},
            ]
        }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        response = self.client.get('/api/serial/setting/device/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(send_data, json.loads(response.data)['serial_device'])


class TestSerialSettingDevice(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.name = 'serial_device'
        self.send_data = {
            '测试1': [
                {defines.RECEIVE_DATA: 'receive1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: 'receive4\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: 'sendA\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: 'sendC\r\n'},
            ]
        }
        data = json.dumps({self.name: self.send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        self.my_serial_data.serial_virtual_device.clear()

    def test_get__one_device__return_right_device(self):
        response = self.client.get('/api/serial/setting/device/' + '测试1')
        self.send_data.pop('测试2')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.send_data, json.loads(response.data)[self.name])

    def test_delete(self):
        response = self.client.delete('/api/serial/setting/device/' + '测试1')
        result = self.client.get('/api/serial/setting/device/')
        self.send_data.pop('测试1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.send_data, json.loads(result.data)[self.name])


class SerialSettingActiveDevice(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.name = 'serial_active_device'
        self.send_data = {
            '测试1': [
                {defines.RECEIVE_DATA: 'receive1\r\n', defines.SEND_DATA: 'send1\r\n'},
                {defines.RECEIVE_DATA: 'receive2\r\n', defines.SEND_DATA: 'send2\r\n'},
                {defines.RECEIVE_DATA: 'receive3\r\n', defines.SEND_DATA: 'send3\r\n'},
                {defines.RECEIVE_DATA: 'receive4\r\n', defines.SEND_DATA: 'send4\r\n'},
            ],
            '测试2': [
                {defines.RECEIVE_DATA: 'receiveA\r\n', defines.SEND_DATA: 'sendA\r\n'},
                {defines.RECEIVE_DATA: 'receiveB\r\n', defines.SEND_DATA: 'sendB\r\n'},
                {defines.RECEIVE_DATA: 'receiveC\r\n', defines.SEND_DATA: 'sendC\r\n'},
            ]
        }
        data = json.dumps({'serial_device': self.send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        self.my_serial_data.serial_virtual_device.clear()

    def test_post(self):
        response = self.client.post('/api/serial/setting/device/active_device/' + '测试1', headers=util.headers)
        result = self.client.get('/api/serial/setting/device/active_device/')
        my_serial_data = serial_manager.SerialData()
        self.assertEqual(my_serial_data.serial_virtual_device['active_device'], '测试1')

        self.assertEqual({'测试1': True}, json.loads(response.data))
        self.assertEqual({'active_device': '测试1'}, json.loads(result.data))

    def test_get(self):
        self.client.post('/api/serial/setting/device/active_device/' + '测试2', headers=util.headers)
        result = self.client.get('/api/serial/setting/device/active_device/')

        self.assertEqual({'active_device': '测试2'}, json.loads(result.data))


def get_test_client():
    app = Flask(__name__,
                static_folder="../static",
                template_folder="../templates")
    my_api = Api(app)
    serial_api.init_api(my_api)
    return app.test_client()


if __name__ == '__main__':
    unittest.main()
