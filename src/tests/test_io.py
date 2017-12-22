import unittest
from ..libs import GPIO as my_gpio
from .. import io_manager
from .. import defines

class TestIo(unittest.TestCase):
    def setUp(self):
        self.io_server = io_manager.IoSetup()
        my_gpio.VERBOSE = False
        self.io_server.set_gpio(my_gpio)

    def tearDown(self):
        pass

    def test_set_io_mode(self):
        self.io_server.set_io_mode()
        self.assertEqual('BOARD', my_gpio.BOARD)

    def test_set_io_type(self):
        self.io_server.set_io_type(io_manager.IoType.input, 'io0')
        self.assertEqual(my_gpio.input)

if __name__ == '__main__':
    unittest.main()
