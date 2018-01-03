import unittest
from flask import Flask
import serial
import json
from unittest import mock
from unittest.mock import patch
from src.app.api import serial_api
from src.hardware import serial_manager

from src.tests import util


class TestSerialSetting(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()
        self.my_serial_setting = serial_manager.SerialSetup()
        self.my_serial_data = serial_manager.SerialData()

    def tearDown(self):
        pass

    # @patch.object(serial_manager.SerialData, 'get_virtual_device')
    def test_get(self):
        # util = SerialTestUtil()
        # util.add_virtual_device(self.my_serial_data)
        # util.set_virtual_device(self.my_serial_data)
        # mock_get_virtual_device.return_value = SerialTestUtil.data
        result = self.client.get('/api/serial/setting/')

        expected = {"serial_setup": {"setting": {"service": {"baudrate": 9600, "serial_port": None, "read_timeout": None, "write_timeout": None},
                                                 "device": {}}}}
        self.assertEqual(200, result.status_code)
        self.assertEqual(expected, json.loads(result.data))


class TestSerialSettingService(unittest.TestCase):
    def setUp(self):
        self.client = get_test_client()

    def tearDown(self):
        pass

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

    def tearDown(self):
        pass

    def test_post__ok_data__return_true(self):
        send_data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
                     '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
                     }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        response = self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        expected = {'测试1': [True, True, True, True], '测试2': [True, True, True]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, json.loads(response.data))

    def test_post__utf8_data__return_false(self):
        send_data = {'测试1': {'错误数据1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', '错误数据2\r\n': 'send4\r\n'},
                     '测试2': {'receiveA\r\n': '错误返回值\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': '错误返回值\r\n'}
                     }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        response = self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)

        excepted = {'测试1': [False, True, True, False], '测试2': [False, True, False]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(excepted, json.loads(response.data))

    def test_get(self):
        send_data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
                     '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
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

    def test_get__one_device__return_right_device(self):
        send_data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
                     '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
                     }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)
        response = self.client.get('/api/serial/setting/device/' + '测试1')
        send_data.pop('测试2')
        self.assertEqual(200, response.status_code)
        self.assertEqual(send_data, json.loads(response.data)['serial_device'])

    def test_delete(self):
        send_data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
                     '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
                     }
        data = json.dumps({'serial_device': send_data}, ensure_ascii=False)
        self.client.post('/api/serial/setting/device/', headers=util.headers, data=data)
        response = self.client.delete('/api/serial/setting/device/' + '测试1')
        result = self.client.get('/api/serial/setting/device/')
        send_data.pop('测试1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(send_data, json.loads(result.data)['serial_device'])


def get_test_client():
    app = serial_api.app
    return app.test_client()


if __name__ == '__main__':
    unittest.main()

# class SerialTestUtil(object):
#     data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
#             '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
#             }
#
#     def add_virtual_device(self, my_serial_data: serial_manager.SerialData):
#         for (k1, v1) in self.data.items():
#             for (k2, v2) in v1.items():
#                 my_serial_data.add_virtual_device_data(k1, k2, v2)
#
#     def set_virtual_device(self, my_serial_data: serial_manager.SerialData):
#         self.add_virtual_device(my_serial_data)
#         my_serial_data.set_active_virtual_device('测试1')
