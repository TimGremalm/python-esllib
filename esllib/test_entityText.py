from unittest import TestCase

from esllib.Package import EntityText
from esllib.enums import FontStylesInv


class TestEntityText(TestCase):
	def test_enity_text_package_args(self):
		self.assertEqual("09010001000200410061", EntityText(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['12px'], text="Aa").__repr__())
		self.assertEqual("0701000100020041", EntityText(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['12px'], text="A").__repr__())
		self.assertEqual("1701000100020059006F0020006D0061006D006D00610021", EntityText(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['12px'], text="Yo mamma!").__repr__())

	def test_enity_text_package_raw(self):
		self.assertEqual("09010001000200410061", EntityText("09010001000200410061").__repr__())
		self.assertEqual("0701000100020041", EntityText("0701000100020041").__repr__())
		self.assertEqual("1701000100020059006F0020006D0061006D006D00610021", EntityText("1701000100020059006F0020006D0061006D006D00610021").__repr__())
