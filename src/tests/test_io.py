import unittest
from unittest import mock
from unittest.mock import patch
from src.hardware.libs import GPIO as my_gpio
from src.hardware import io_manager
from src.hardware import defines

test_data = {
    'input': [{"io_number": "io0", "io_name": "输入测试1"},
              {"io_number": "io1", "io_name": "输入测试2"},
              {"io_number": "io2", "io_name": "输入测试3"},
              {"io_number": "io3", "io_name": "输入测试4"},
              {"io_number": "io4", "io_name": "输入测试5"},
              {"io_number": "io5", "io_name": "输入测试6"},
              {"io_number": "io6", "io_name": "输入测试7"}
              ],
    'output': [{"io_number": "io8", "io_name": "输出测试1"},
               {"io_number": "io9", "io_name": "输出测试2"},
               {"io_number": "io10", "io_name": "输出测试3"},
               {"io_number": "io11", "io_name": "输出测试4"},
               {"io_number": "io12", "io_name": "输出测试5"},
               {"io_number": "io13", "io_name": "输出测试6"},
               {"io_number": "io14", "io_name": "输出测试7"}
               ],
    'notset': [{'io_number': 'io7', "io_name": ""},
               {"io_number": "io15", "io_name": ""}
               ]
}


class TestIoSetup(unittest.TestCase):
    def setUp(self):
        self.io_server = io_manager.IoSetup()
        my_gpio.VERBOSE = False
        self.io_server.set_gpio(my_gpio)

    def tearDown(self):
        self.io_server.io_cleanup_setup()

    def test_set_io_mode(self):
        self.io_server.set_io_mode()
        self.assertEqual('BOARD', my_gpio.BOARD)

    def test_set_io_type_input(self):
        self.io_server.set_io_type(io_manager.IoType.input, 'io0')
        self.io_server.set_io_type(io_manager.IoType.input, 'io3')

        result = self.io_server.get_io_type(io_manager.IoType.input)
        self.assertEqual('io0', result[0])
        self.assertEqual('io3', result[1])

    def test_set_io_type_output(self):
        self.io_server.set_io_type(io_manager.IoType.output, 'io8')
        self.io_server.set_io_type(io_manager.IoType.output, 'io9')
        result = self.io_server.get_io_type(io_manager.IoType.output)
        self.assertEqual('io8', result[0])
        self.assertEqual('io9', result[1])

    def test_set_io_list_input(self):
        io_list = ['io0', 'io3', 'io10', 'io15']
        self.io_server.set_io_list(io_manager.IoType.input, io_list)
        result = self.io_server.get_io_type(io_manager.IoType.input)
        self.assertEqual(io_list, result)

    def test_set_io_list_output(self):
        io_list = ['io0', 'io3', 'io10', 'io15']
        self.io_server.set_io_list(io_manager.IoType.output, io_list)
        result = self.io_server.get_io_type(io_manager.IoType.output)
        self.assertEqual(io_list, result)

    def test_set_io_name(self):
        self.io_server.set_io_name('io0', '测试1')
        self.io_server.set_io_name('io1', '测试2')
        result0 = self.io_server.io_name.get('io0')
        result1 = self.io_server.io_name.get('io1')
        self.assertEqual('测试1', result0)
        self.assertEqual('测试2', result1)

    def test_get_io_name__one_name__return_one_name(self):
        self.io_server.set_io_name('io3', '测试3')
        self.io_server.set_io_name('io5', '测试5')
        result = self.io_server.get_io_name('io3')
        self.assertEqual('测试3', result)

    def test_get_io_name__all_io__return_all_name(self):
        self.io_server.set_io_name('io0', '测试1')
        self.io_server.set_io_name('io1', '测试2')
        self.io_server.set_io_name('io15', '测试15')
        io_name = dict(io0='测试1', io1='测试2', io2='', io3='',
                       io4='', io5='', io6='', io7='',
                       io8='', io9='', io10='', io11='',
                       io12='', io13='', io14='', io15='测试15')
        result = self.io_server.get_io_name()

        self.assertEqual(io_name, result)

    def test_get_io_setting(self):
        for io_type, io_data_list in test_data.items():
            for io_data in io_data_list:
                self.io_server.set_io_type(io_manager.IoType[io_type], io_data.get('io_number'))
                self.io_server.set_io_name(io_data.get('io_number'), io_data.get('io_name'))
        result = self.io_server.get_io_setting()
        self.assertEqual(test_data, result)

    def test_io_cleanup_setup__clean_type_and_name__no_type_and_name(self):
        io_list = ['io0', 'io3', 'io10', 'io15']
        self.io_server.set_io_list(io_manager.IoType.output, io_list)
        self.io_server.set_io_name('io3', '测试3')
        self.io_server.set_io_name('io15', '测试15')
        self.io_server.io_cleanup_setup('io3')
        io_list.pop(1)
        result = self.io_server.get_io_type(io_manager.IoType.output)
        result_name = self.io_server.get_io_name()
        self.assertEqual(io_list, result)
        self.assertEqual('', result_name.get('io3'))
        self.assertEqual('测试15', result_name.get('io15'))

    def test_io_cleanup_setup__with_data(self):
        io_list = ['io0', 'io3', 'io10', 'io15']
        self.io_server.set_io_list(io_manager.IoType.output, io_list)
        io_data = io_manager.IoData()
        io_data.set_outputs_data(io_list, True)
        self.io_server.io_cleanup_setup('io3')
        io_list.pop(1)
        result = self.io_server.get_io_type(io_manager.IoType.output)
        self.assertEqual(io_list, result)

    # 用mock_add_event_detect代替GPIO中的add_event_detect
    @patch.object(my_gpio, 'add_event_detect')
    def test_set_edge_callback(self, mock_add_event_detect):
        self.io_server.set_io_type(io_manager.IoType.input, 'io1')
        mock_add_event_detect.return_value = True
        mock_callback_function = mock.MagicMock()
        result = self.io_server.set_edge_callback('io1', io_manager.EdgeType.raising, mock_callback_function)
        mock_add_event_detect.assert_called_once_with(defines.io_defines['io1'], my_gpio.RISING, callback=mock_callback_function)
        self.assertEqual((True, 'io1'), result)
        # 如果可以模拟一下RISING的话，可以测试一下mock_function是否被调用了2次
        # call_count = mock_callback_function.call_count


class TestIoData(unittest.TestCase):
    def setUp(self):
        self.io_server = io_manager.IoSetup()
        self.io_data = io_manager.IoData()
        my_gpio.VERBOSE = False
        self.io_server.set_gpio(my_gpio)

    def tearDown(self):
        self.io_server.io_cleanup_setup()

    def test_set_output_data__use_output__return_true(self):
        io_number1 = 'io1'
        io_number2 = 'io2'
        self.io_server.set_io_list(io_manager.IoType.output, (io_number1, io_number2))
        self.io_data.set_output_data(io_number1, True)
        result1 = self.io_data.get_data(io_number1)

        self.io_data.set_output_data(io_number2, False)
        result2 = self.io_data.get_data(io_number2)

        self.assertEqual({io_number1: True}, result1)
        self.assertEqual({io_number2: False}, result2)

        # 在清除io设置后检查程序是否正确
        self.io_server.io_cleanup_setup()
        result = self.io_data.get_data(io_number1)
        self.assertEqual({io_number1: '输出接口' + io_number1 + "没有初始化"}, result)

    def test_set_output_data__use_input_io__return_false(self):
        io_number = 'io1'
        self.io_server.set_io_type(io_manager.IoType.input, io_number)
        result = self.io_data.set_output_data(io_number, True)
        self.assertEqual((False, io_number + "不是输出接口，无法设置"), result)

    def test_set_outputs_data__use_high_level__return_true(self):
        io_list = ['io1', 'io3', 'io15']
        self.io_server.set_io_list(io_manager.IoType.output, io_list)
        result1 = self.io_data.set_outputs_data(io_list, True)
        result2 = self.io_data.get_data_list(io_list)

        self.assertEqual([(True, 'io1'), (True, 'io3'), (True, 'io15')], result1)
        self.assertEqual({'io1': True, 'io3': True, 'io15': True}, result2)

    def test_set_outputs_data__use_low_level__return_true(self):
        io_list = ['io1', 'io3', 'io15']
        self.io_server.set_io_list(io_manager.IoType.output, io_list)
        result1 = self.io_data.set_outputs_data(io_list, False)
        result2 = self.io_data.get_data_list(io_list)

        self.assertEqual([(True, 'io1'), (True, 'io3'), (True, 'io15')], result1)
        self.assertEqual({'io1': False, 'io3': False, 'io15': False}, result2)

    # 使用mock代替GPIO
    @patch.object(my_gpio, 'input')
    def test_get_data__get_input_data__return_input_data(self, mock_input):
        io_number = 'io15'
        mock_input.return_value = True
        self.io_server.set_io_type(io_manager.IoType.input, io_number)
        result = self.io_data.get_data(io_number)

        mock_input.assert_called_once_with(defines.io_defines[io_number])
        self.assertEqual({'io15': True}, result)

    @patch.object(my_gpio, 'output')
    def test_get_data__get_output_data__return_output_data(self, mock_output):
        io_number = 'io15'
        mock_output.return_value = True
        self.io_server.set_io_type(io_manager.IoType.output, io_number)
        self.io_data.set_output_data(io_number, True)
        result = self.io_data.get_data(io_number)

        # mock_output.setup.assert_called_once_with(defines.io_defines[io_number], mock_output.OUT)
        self.assertEqual({'io15': True}, result)

    # 使用mock代替GPIO
    @patch.object(my_gpio, 'input')
    def test_get_data_list__get_input_data__return_input_data(self, mock_input):
        io_list = ['io1', 'io3', 'io15']
        mock_input.return_value = True
        self.io_server.set_io_list(io_manager.IoType.input, io_list)
        result = self.io_data.get_data_list(io_list)

        # 检查mock的函数调用了哪些参数
        expected = '[call(' + str(defines.io_defines[io_list[0]]) + '),' + \
                   ' call(' + str(defines.io_defines[io_list[1]]) + '),' + \
                   ' call(' + str(defines.io_defines[io_list[2]]) + ')]'

        self.assertEqual(len(io_list), mock_input.call_count)
        self.assertEqual(expected, str(mock_input.call_args_list))
        self.assertEqual({'io1': True, 'io3': True, 'io15': True}, result)


if __name__ == '__main__':
    unittest.main()
