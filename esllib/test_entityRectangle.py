from unittest import TestCase

from esllib.Package import EntityRectangle


class TestEntityRectangle(TestCase):
	def test_entity_rectangle_args(self):
		self.assertEqual("0B0100016400003200320001", EntityRectangle(vertical=1, horizontal=1, draw_style=0, height=50, width=50, border=1).__repr__())

	def test_entity_rectangle_raw(self):
		self.assertEqual("0B0100016400003200320001", EntityRectangle("0B0100016400003200320001").__repr__())
