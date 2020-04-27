from unittest import TestCase
from esllib.Package import EntityLEDData


class TestEntityLEDData(TestCase):
	def test_led_data_package_args(self):
		self.assertEqual("07044E2E00ED0003", EntityLEDData(color_red=False, color_green=False, color_blue=True, service_code=20014, flash_times=3).__repr__())
		self.assertEqual("07024E2300ED0004", EntityLEDData(color_red=False, color_green=True, color_blue=False, service_code=20003, flash_times=4).__repr__())

	def test_led_data_package_raw(self):
		self.assertEqual("07044E2E00ED0003", EntityLEDData("07044E2E00ED0003").__repr__())
		self.assertEqual("07024E2300ED0004", EntityLEDData("07024E2300ED0004").__repr__())
