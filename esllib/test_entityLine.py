from unittest import TestCase

from esllib.Package import EntityLine
from esllib.enums import FontStylesInv


class TestEntityLine(TestCase):
	def test_entity_line_args(self):
		self.assertEqual("0701000100620001", EntityLine(vertical=1, horizontal=1, draw_style=0, font_style=FontStylesInv["Horizontal Line"], border=1).__repr__())

	def test_entity_line_raw(self):
		self.assertEqual("0701000100620001", EntityLine("0701000100620001").__repr__())
