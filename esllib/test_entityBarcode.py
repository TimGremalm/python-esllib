from unittest import TestCase

from esllib.Package import EntityBarcode
from esllib.enums import FontStylesInv


class TestEntityBarcode(TestCase):
	def test__enity_barcode_package_args(self):
		self.assertEqual("0D0100010042008800370038008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode 128'], text="7").__repr__())
		self.assertEqual("0D0100010042008800380039008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode 128'], text="8").__repr__())
		self.assertEqual("0D010001004200880039003A008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode 128'], text="9").__repr__())
		self.assertEqual("0F01000100420088003100300052008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode 128'], text="10").__repr__())
		self.assertEqual("25010001004100880037003300310031003200350030003000300039003400310039003D008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode EAN13'], text="731125000941").__repr__())
		self.assertEqual("25010001004900880037003300310031003200350030003000300039003400310039003D008A", EntityBarcode(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv['Barcode EAN13 Double Size'], text="731125000941").__repr__())

	def test__enity_barcode_package_raw(self):
		self.assertEqual("0D0100010042008800370038008A", EntityBarcode("0D0100010042008800370038008A").__repr__())
		self.assertEqual("0D0100010042008800380039008A", EntityBarcode("0D0100010042008800380039008A").__repr__())
		self.assertEqual("0D010001004200880039003A008A", EntityBarcode("0D010001004200880039003A008A").__repr__())
		self.assertEqual("0F01000100420088003100300052008A", EntityBarcode("0F01000100420088003100300052008A").__repr__())
		self.assertEqual("25010001004100880037003300310031003200350030003000300039003400310039003D008A", EntityBarcode("25010001004100880037003300310031003200350030003000300039003400310039003D008A").__repr__())
		self.assertEqual("25010001004900880037003300310031003200350030003000300039003400310039003D008A", EntityBarcode("25010001004900880037003300310031003200350030003000300039003400310039003D008A").__repr__())
