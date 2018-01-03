import unittest
import serial
from unittest import mock
from unittest.mock import patch
from src.hardware import serial_manager
from src.hardware import defines


class TestSerialSetup(unittest.TestCase):
    def setUp(self):
        self.my_ser = serial_manager.SerialSetup()

    def tearDown(self):
        pass

    def test_set_baudrate__use_right_data__return_true(self):
        self.my_ser.set_baudrate(19200)
        r1 = self.my_ser.get_serial().baudrate
        result = self.my_ser.set_baudrate(115200)
        r2 = self.my_ser.get_serial().baudrate
        self.assertEqual(True, result)
        self.assertEqual(19200, r1)
        self.assertEqual(115200, r2)

    def test_set_baudrate__use_wrong_data__return_False(self):
        result = self.my_ser.set_baudrate(500)
        r2 = self.my_ser.get_serial().baudrate
        self.assertEqual(False, result)
        self.assertNotEqual(500, r2)

    def test_set_write_timeout__use_right_data__return_true(self):
        result = self.my_ser.set_write_timeout(100)
        self.assertEqual(True, result)

    def test_set_write_timeout__use_wrong_data__return_true(self):
        result = self.my_ser.set_write_timeout(10)
        self.assertEqual(False, result)

    def test_set_read_timeout__use_right_data__return_true(self):
        result = self.my_ser.set_read_timeout(100)
        self.assertEqual(True, result)

    def test_set_read_timeout__use_wrong_data__return_true(self):
        result = self.my_ser.set_read_timeout(10)
        self.assertEqual(False, result)


class TestSerialData(unittest.TestCase):
    def setUp(self):
        self.my_ser = serial_manager.SerialSetup()
        self.my_data = serial_manager.SerialData()

    def tearDown(self):
        # 如果不这样clear的话，这个静态变量一直都会存在。todo: 需要确认一下为啥这个静态变量不会自动释放掉并且赋None也不行
        self.my_data.serial_virtual_device.clear()

    def test_add_virtual_device_data__use_string__return_true(self):
        device_name = 'test_device'
        receive_data = 'receive'
        send_data = 'send'
        result = self.my_data.add_virtual_device_data(device_name, receive_data, send_data)
        result_data = self.my_data.serial_virtual_device[device_name][receive_data]
        self.assertEqual(True, result)
        self.assertEqual(send_data, result_data)

    def test_add_virtual_device_data__use_crlf__return_true(self):
        device_name = 'test_device'
        receive_data = 'receive\r\n'
        send_data = 'send\r\n'

        result = self.my_data.add_virtual_device_data(device_name, receive_data, send_data)
        result_data = self.my_data.serial_virtual_device[device_name][receive_data]
        self.assertEqual(True, result)
        self.assertEqual(send_data, result_data)

    def test_add_virtual_device_data__use_unicode_data__return_false(self):
        device_name = '测试'
        receive_data = '接收'
        send_data = '发送'

        result = self.my_data.add_virtual_device_data(device_name, receive_data, send_data)
        self.assertEqual(False, result)

    def test_add_virtual_device_data__use_unicode_name_and_multiple_data__return_true(self):
        data = {'测试1': {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'},
                '测试2': {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
                }
        result = []
        for (k1, v1) in data.items():
            for (k2, v2) in v1.items():
                result.append(self.my_data.add_virtual_device_data(k1, k2, v2))
        self.assertEqual([True, True, True, True, True, True, True], result)

        devices = self.my_data.get_virtual_device()
        for (k1, v1) in data.items():
            for (k2, v2) in v1.items():
                self.assertEqual(v2, devices[k1][k2])

    def test_set_virtual_device(self):
        device_name = '测试1'
        data = {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'}
        result = self.my_data.set_virtual_device(device_name, data)

        self.assertEqual([True, True, True, True], result)
        devices = self.my_data.get_virtual_device()
        for (k2, v2) in devices['测试1'].items():
            self.assertEqual(v2, devices['测试1'][k2])

    def test_delete_virtual_device(self):
        device_name1 = '测试1'
        data1 = {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'}
        device_name2 = '测试2'
        data2 = {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n', 'receiveC\r\n': 'sendC\r\n'}
        self.my_data.set_virtual_device(device_name1, data1)
        self.my_data.set_virtual_device(device_name2, data2)
        self.my_data.delete_virtual_device(device_name1)

        result = self.my_data.get_virtual_device()
        self.assertEqual({device_name2: data2}, result)

    def test_get_respond_data__from_active_device__return_correct_data(self):
        device_name1 = '测试1'
        device_name2 = '测试2'
        data1 = {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'}
        data2 = {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n'}
        self.my_data.set_virtual_device(device_name1, data1)
        self.my_data.set_virtual_device(device_name2, data2)
        self.my_data.set_active_virtual_device(device_name1)

        result = self.my_data.get_response_data('receive1\r\n')
        expected = data1.get('receive1\r\n')
        self.assertEqual(True, result[0])
        self.assertEqual(expected, result[1])

    def test_get_respond_data__from_not_active_device__return_false(self):
        device_name1 = '测试1'
        device_name2 = '测试2'
        data1 = {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'}
        data2 = {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n'}
        self.my_data.set_virtual_device(device_name1, data1)
        self.my_data.set_virtual_device(device_name2, data2)
        self.my_data.set_active_virtual_device(device_name1)

        result = self.my_data.get_response_data('receiveA\r\n')
        self.assertEqual(False, result[0])
        self.assertEqual('receiveA\r\n', result[1])


class TestResponseRequests(unittest.TestCase):
    def setUp(self):
        self.my_serial = serial_manager.SerialSetup()
        self.my_data = serial_manager.SerialData()
        self.my_response = serial_manager.ResponseRequests(self.my_serial.get_serial())
        pass

    def tearDown(self):
        self.my_data.serial_virtual_device.clear()
        pass

    @patch.object(serial, "Serial")
    def test_send_serial_data__use_correct_data__return_true(self, my_mock_serial):
        my_response = serial_manager.ResponseRequests(my_mock_serial)
        result = my_response.send_serial_data("test1")
        self.assertEqual(True, result[0])
        my_mock_serial.write.assert_called_once_with(b"test1")

    @patch.object(serial, "Serial")
    def test_send_serial_data__use_wrong_data__return_false(self, my_mock_serial):
        my_response = serial_manager.ResponseRequests(my_mock_serial)
        result = my_response.send_serial_data("数据")
        self.assertEqual(False, result[0])
        self.assertEqual('ordinal not in range(128)', result[1].reason)
        self.assertEqual(0, my_mock_serial.write.call_count)

    @patch.object(serial, "Serial")
    def test_send_serial_data__use_int_data__return_true(self, my_mock_serial):
        my_response = serial_manager.ResponseRequests(my_mock_serial)
        result = my_response.send_serial_data(11)
        self.assertEqual(True, result[0])
        my_mock_serial.write.assert_called_once_with(11)

    @patch.object(serial, "Serial")
    def test_read_respond_data(self, my_mock_serial):
        device_name1 = '测试1'
        device_name2 = '测试2'
        data1 = {'receive1\r\n': 'send1\r\n', 'receive2\r\n': 'send2\r\n', 'receive3\r\n': 'send3\r\n', 'receive4\r\n': 'send4\r\n'}
        data2 = {'receiveA\r\n': 'sendA\r\n', 'receiveB\r\n': 'sendB\r\n'}
        self.my_data.set_virtual_device(device_name1, data1)
        self.my_data.set_virtual_device(device_name2, data2)
        self.my_data.set_active_virtual_device(device_name1)

        self.my_response.my_data = self.my_data
        self.my_response.set_serial(my_mock_serial)
        result = self.my_response.read_respond_data(b"receive1\r\n")
        my_mock_serial.write.assert_called_once_with(b'send1\r\n')
        self.assertEqual((True, b"send1\r\n"), result)


if __name__ == '__main__':
    unittest.main()
