from unittest import TestCase

from PIL import Image, ImageDraw
from esllib.Package import EntityImage

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)


class TestEntityImage(TestCase):
	def test_entity_image_line_top_left(self):
		def image_blackline_topleft(pixels: int) -> Image:
			imggout = Image.new('RGB', (400, 300), "white")
			draw = ImageDraw.Draw(imggout)
			draw.line((0, 0, pixels-1, 0), fill=black, width=1)
			# imggout.save("test.bmp")
			return imggout
		self.assertEqual("FC00000000012B018F00000007C000FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(1), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000007E000FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(2), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000007F000FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(3), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000007F800FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(4), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000007FC00FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(5), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000007FE00FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(6), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F000000074700FFFF00BAD4", EntityImage(x=0, y=0, image=image_blackline_topleft(7), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F000000074800FFFF00B9D4", EntityImage(x=0, y=0, image=image_blackline_topleft(8), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F000000074900FFFF00B8D4", EntityImage(x=0, y=0, image=image_blackline_topleft(9), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F000000075E00FFFF00A3D4", EntityImage(x=0, y=0, image=image_blackline_topleft(30), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F000000075F00FFFF00A2D4", EntityImage(x=0, y=0, image=image_blackline_topleft(31), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000008412000FFFF00A1D4", EntityImage(x=0, y=0, image=image_blackline_topleft(32), colored_image=False).__repr__())
		self.assertEqual("FC00000000012B018F00000008412100FFFF00A0D4", EntityImage(x=0, y=0, image=image_blackline_topleft(33), colored_image=False).__repr__())

	def test_entity_image_multiple_lines(self):
		img = Image.new('RGB', (400, 300), "white")
		def image_lines_from_list(input_img: Image, input_lines: list) -> Image:
			pixel_access = input_img.load()
			counter = 0
			for count, color in input_lines:
				for i in range(count):
					x = counter % input_img.width
					y = int(counter / input_img.width)
					if color:
						pixel_access[x, y] = color
					counter += 1
		image_lines_from_list(img,
								[(31, black), (31, white), (32, black), (32, white), (33, black), (241, white),
								(256, black), (31, white), (113, black),
								(256, white), (512, black), (118432, white)])
		# Test the black part
		self.assertEqual("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CE",
							EntityImage(x=0, y=0, image=img, colored_image=False).__repr__())
		# Test both black and red part, the red part should be completly blank because no red pixels have been drawn
		self.assertEqual("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CEFC80000000812B018F0000000600FFFF00C1D4",
							EntityImage(x=0, y=0, image=img, colored_image=True).__repr__())
		# Now, draw som red lines
		image_lines_from_list(img, [(8095, None), (31, red), (8, white), (256, red), (65535, white), (46075, white)])
		# Test black part and the new aditions to the red part
		self.assertEqual("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CEFC80000000812B018F0000000E009F1F5F0840000100FFFF00FBB3",
							EntityImage(x=0, y=0, image=img, colored_image=True).__repr__())

	def test_entity_image_raw(self):
		self.assertEqual("FC00000000012B018F00000007C000FFFF00BAD4", EntityImage("FC00000000012B018F00000007C000FFFF00BAD4").__repr__())  # 1px
		self.assertEqual("FC00000000012B018F00000007E000FFFF00BAD4", EntityImage("FC00000000012B018F00000007E000FFFF00BAD4").__repr__())  # 2px
		self.assertEqual("FC00000000012B018F00000007F000FFFF00BAD4", EntityImage("FC00000000012B018F00000007F000FFFF00BAD4").__repr__())  # 3px
		self.assertEqual("FC00000000012B018F00000007F800FFFF00BAD4", EntityImage("FC00000000012B018F00000007F800FFFF00BAD4").__repr__())  # 4px
		self.assertEqual("FC00000000012B018F00000007FC00FFFF00BAD4", EntityImage("FC00000000012B018F00000007FC00FFFF00BAD4").__repr__())  # 5px
		self.assertEqual("FC00000000012B018F00000007FE00FFFF00BAD4", EntityImage("FC00000000012B018F00000007FE00FFFF00BAD4").__repr__())  # 6px
		self.assertEqual("FC00000000012B018F000000074700FFFF00BAD4", EntityImage("FC00000000012B018F000000074700FFFF00BAD4").__repr__())  # 7px
		self.assertEqual("FC00000000012B018F000000074800FFFF00B9D4", EntityImage("FC00000000012B018F000000074800FFFF00B9D4").__repr__())  # 8px
		self.assertEqual("FC00000000012B018F000000074900FFFF00B8D4", EntityImage("FC00000000012B018F000000074900FFFF00B8D4").__repr__())  # 9px
		self.assertEqual("FC00000000012B018F000000075E00FFFF00A3D4", EntityImage("FC00000000012B018F000000075E00FFFF00A3D4").__repr__())  # 30px
		self.assertEqual("FC00000000012B018F000000075F00FFFF00A2D4", EntityImage("FC00000000012B018F000000075F00FFFF00A2D4").__repr__())  # 31px
		self.assertEqual("FC00000000012B018F00000008412000FFFF00A1D4", EntityImage("FC00000000012B018F00000008412000FFFF00A1D4").__repr__())  # 32px
		self.assertEqual("FC00000000012B018F00000008412100FFFF00A0D4", EntityImage("FC00000000012B018F00000008412100FFFF00A0D4").__repr__())  # 33px
		self.assertEqual("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CE", EntityImage("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CE").__repr__())  # Black lines different lengths
		self.assertEqual("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CEFC80000000812B018F0000000E009F1F5F0840000100FFFF00FBB3",EntityImage("FC00000000012B018F0000001C5F1F41200120412101F14000011F417100000140000200FFFF00A1CEFC80000000812B018F0000000E009F1F5F0840000100FFFF00FBB3").__repr__())  # Black & red lines different lengths
