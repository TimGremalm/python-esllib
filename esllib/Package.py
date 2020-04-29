from esllib.barcode import validate_barcode128b_characters, validate_ean13_characters, \
	calculate_barcode128b_check_digit, calculate_ean13_check_digit
from esllib.conversion import int_to_hexstring, hexstring_to_int, utf8_to_utf16hexstring, utf16hexstring_to_utf8
from esllib.enums import AnswerTagStatus, DrawStyles, FontStyles, FontStylesInv


class EntityText:
	"""
	Text entity

	Part					Length	Data
	DataLength				2		07(7*2=14 bytes length of following segment) 15(21*2=42B)
	Vertical				3		010(1), 020(2), FF0(255), 001(256), FF1(511), 002(512)
	Horizontal				3		001(1), 003(3), 0FF(255), 1FF(511), 200(512)
	DrawStyle				2		00(Normal), 55(Red), AA(Red and Inversed FG BG), FF(Inverse FG BG)
	FontStyle				2		See Font Styles
	Text							0041(A) UTF-16 00410042(AB)
	"""
	def __init__(self, raw="", vertical=0, horizontal=0, draw_style=0, font_style=0, text=""):
		if len(raw) > 0:
			self._raw = raw
			self.length = hexstring_to_int(self._raw[0:2], little_endian=False)*2
			if len(self._raw) != self.length+2:
				raise Exception(f'Answer package is always a 23 byte string, this string is {len(self._raw)} Packet: {self._raw}')
			self.vertical = hexstring_to_int(self._raw[2:5], little_endian=True)
			self.horizontal = hexstring_to_int(self._raw[5:8], little_endian=False)
			self.draw_style = hexstring_to_int(self._raw[8:10], little_endian=False)
			self.font_style = hexstring_to_int(self._raw[10:12], little_endian=False)
			self.text = utf16hexstring_to_utf8(self._raw[12:])
		else:
			self.length = 0
			self.vertical = vertical
			self.horizontal = horizontal
			self.draw_style = draw_style
			self.font_style = font_style
			self.text = text

	def __repr__(self):
		"""
		Build and return a text entity package
		:return: str representing entity
		"""
		# Start with packet, then add length of packet
		out = ""
		out += int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3)
		out += int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3)
		out += int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += utf8_to_utf16hexstring(self.text)
		length = int_to_hexstring(int(len(out)/2), little_endian=False, number_of_hex_digits=2)
		out = length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		out = "Entity Text package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		length = len(self.__repr__())-2
		out += "DataLengthSegment\t\t2\t\t%s (%d*2=%d bytes)\n" % (int_to_hexstring(int(length/2), little_endian=False, number_of_hex_digits=2), int(length/2), length)
		out += "Vertical\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3), self.vertical)
		out += "Horizontal\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3), self.horizontal)
		if self.draw_style in DrawStyles:
			out += "DrawStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2), DrawStyles[self.draw_style])
		else:
			out += "DrawStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		if self.font_style in FontStyles:
			out += "FontStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2), FontStyles[self.font_style])
		else:
			out += "FontStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += "Text\t\t\t\t\t\t\t%s (%s)" % (utf8_to_utf16hexstring(self.text), self.text)
		return out


class EntityBarcode:
	"""
	Barcode entity, the same as text except font style is set to bar code

	Part					Length	Data
	DataLength				2		07(7*2=14 bytes length of following segment) 15(21*2=42B)
	Vertical				3		010(1), 020(2), FF0(255), 001(256), FF1(511), 002(512)
	Horizontal				3		001(1), 003(3), 0FF(255), 1FF(511), 200(512)
	DrawStyle				2		00(Normal), 55(Red), AA(Red and Inversed FG BG), FF(Inverse FG BG)
	FontStyle				2		See Font Styles
	Text							0041(A) UTF-16 00410042(AB)
	41(Barcode EAN13) Start Code B 0088(UTF-16 HTS), Encoded data (Ex. 0037 7 0033 3 0031 1 0031 1 0032 2 0035 5 0030 0 0030 0 0030 0 0039 9 0034 4 0031 1), Check Digit (Ex. 0039 9), Stop 003D 008A(UTF-16 VTS)
	42(Barcode 128) Start Code B 0088(UTF-16 HTS), Encoded data (Ex. 0031 1, 0030 0), Check Digit (Ex. 0052 R), Stop 008A(UTF-16 VTS)
	"""
	def __init__(self, raw="", vertical=0, horizontal=0, draw_style=0, font_style=0, text=""):
		# Barcodes that is supported now, some other check digits etc. might be needed
		self.supported_barcodes = [FontStylesInv['Barcode EAN13'], FontStylesInv['Barcode 128'], FontStylesInv['Barcode EAN13 Double Size'], FontStylesInv['Barcode 128 Double Size']]
		if len(raw) > 0:
			self._raw = raw
			self.length = hexstring_to_int(self._raw[0:2], little_endian=False)*2
			if len(self._raw) != self.length+2:
				raise Exception(f'Barcode packet length field does not match up with actual size, this string is {len(self._raw)} Packet: {self._raw}')
			self.vertical = hexstring_to_int(self._raw[2:5], little_endian=True)
			self.horizontal = hexstring_to_int(self._raw[5:8], little_endian=False)
			self.draw_style = hexstring_to_int(self._raw[8:10], little_endian=False)
			self.font_style = hexstring_to_int(self._raw[10:12], little_endian=False)
			rawtext = self._raw[12:]
			if self.font_style in [FontStylesInv['Barcode 128'], FontStylesInv['Barcode 128 Double Size']]:
				self.text = rawtext[4:-8]  # Skip first start code, and last check digit and stop
			if self.font_style in [FontStylesInv['Barcode EAN13'], FontStylesInv['Barcode EAN13 Double Size']]:
				if len(rawtext) != (1*4)+(13*4)+(2*4):
					raise Exception("Can't read EAN 13, expected length to be 1 start + 13 digits + 2 stop.")
				self.text = rawtext[4:-12]  # Skip first start code, and last check digit and stop
			self.text = utf16hexstring_to_utf8(self.text)
		else:
			self.length = 0
			self.vertical = vertical
			self.horizontal = horizontal
			self.draw_style = draw_style
			self.font_style = font_style
			self.text = text
		self.prefix = "0088"  # Start Code B 0088(UTF-16 HTS), also used by EAN 13
		if self.font_style not in self.supported_barcodes:
			raise Exception("Only Barcode 128 and EAN13 is supported.")
		# Barcode 128
		if self.font_style in [FontStylesInv['Barcode 128'], FontStylesInv['Barcode 128 Double Size']]:
			if len(self.text) < 1:
				raise Exception("Barcode 128 musbe more than 0 cahracters.")
			if not validate_barcode128b_characters(self.text):
				raise Exception("Only characters belonging to Barcode 128 B is valid.")
			self.suffix = utf8_to_utf16hexstring(calculate_barcode128b_check_digit(self.text))
			self.suffix += "008A"  # Stop 008A(UTF-16 VTS)
		# EAN 13
		if self.font_style in [FontStylesInv['Barcode EAN13'], FontStylesInv['Barcode EAN13 Double Size']]:
			if len(self.text) != 12:
				raise Exception("EAN 13 must bra 12 digits, the 13th is check digit and it will be calculated automatically.")
			if not validate_ean13_characters(self.text):
				raise Exception("EAN 13 can only contain digits.")
			self.suffix = utf8_to_utf16hexstring(calculate_ean13_check_digit(self.text))
			self.suffix += "003D"  # Hardcoded for EAN13?
			self.suffix += "008A"  # Stop 008A(UTF-16 VTS)

	def __repr__(self):
		"""
		Build and return a barcode entity package
		:return: str representing entity
		"""
		# Start with packet, then add length of packet
		out = ""
		out += int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3)
		out += int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3)
		out += int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += self.prefix
		out += utf8_to_utf16hexstring(self.text)
		out += self.suffix
		length = int_to_hexstring(int(len(out)/2), little_endian=False, number_of_hex_digits=2)
		out = length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		out = "Entity Barcode package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		length = len(self.__repr__())-2
		out += "DataLengthSegment\t\t2\t\t%s (%d*2=%d bytes)\n" % (int_to_hexstring(int(length/2), little_endian=False, number_of_hex_digits=2), int(length/2), length)
		out += "Vertical\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3), self.vertical)
		out += "Horizontal\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3), self.horizontal)
		if self.draw_style in DrawStyles:
			out += "DrawStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2), DrawStyles[self.draw_style])
		else:
			out += "DrawStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		if self.font_style in FontStyles:
			out += "FontStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2), FontStyles[self.font_style])
		else:
			out += "FontStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += "Prefix\t\t\t\t\t\t\t%s (Start code)\n" % self.prefix
		out += "Text\t\t\t\t\t\t\t%s (%s)\n" % (utf8_to_utf16hexstring(self.text), self.text)
		out += "Suffix\t\t\t\t\t\t\t%s (Check Digit and Stop code)" % self.suffix
		return out


class EntityRectangle:
	"""
	Rectangle entity, no support in Demo Tool

	Part					Length	Data
	DataLengthSegment		2		0B(11*2=22 bytes for rectangle)
	Vertical				3		010(1), 020(2), FF0(255), 001(256), FF1(511), 002(512)
	Horizontal				3		001(1), 003(3), 0FF(255), 1FF(511), 200(512)
	FontStyle				2		64(Rectangle?)
	DrawStyle				2		00(Normal), 55(Red), AA(Red and Inversed FG BG), FF(Inverse FG BG)
	Height					4		0032(50px?)
	Width					4		0032(50px?)
	Border?					4		0000 (Hardcoded?)
	"""
	def __init__(self, raw="", vertical=0, horizontal=0, draw_style=0, height=0, width=0, border=0):
		if len(raw) > 0:
			self._raw = raw
			self.length = hexstring_to_int(self._raw[0:2], little_endian=False)*2
			if self.length != 22:
				raise Exception(f'Rectangle package is always 2+22 byte.')
			self.vertical = hexstring_to_int(self._raw[2:5], little_endian=True)
			self.horizontal = hexstring_to_int(self._raw[5:8], little_endian=False)
			self.font_style = hexstring_to_int(self._raw[8:10], little_endian=False)
			if self.font_style != FontStylesInv['Rectangle']:
				raise Exception(f'Font style must be 0x64(Rectangle) in a Rectangle package.')
			self.draw_style = hexstring_to_int(self._raw[10:12], little_endian=False)
			self.height = hexstring_to_int(self._raw[12:16], little_endian=False)
			self.width = hexstring_to_int(self._raw[16:20], little_endian=False)
			self.border = hexstring_to_int(self._raw[20:24], little_endian=False)
		else:
			self.length = 0
			self.vertical = vertical
			self.horizontal = horizontal
			self.font_style = FontStylesInv['Rectangle']
			self.draw_style = draw_style
			self.height = height
			self.width = width
			self.border = border

	def __repr__(self):
		"""
		Build and return a rectangle entity package
		:return: str representing entity
		"""
		# Start with packet, then add length of packet
		out = ""
		out += int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3)
		out += int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3)
		out += int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.height, little_endian=False, number_of_hex_digits=4)
		out += int_to_hexstring(self.width, little_endian=False, number_of_hex_digits=4)
		out += int_to_hexstring(self.border, little_endian=False, number_of_hex_digits=4)
		length = int_to_hexstring(int(len(out)/2), little_endian=False, number_of_hex_digits=2)
		out = length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		out = "Entity Rectangle package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		length = len(self.__repr__())-2
		out += "DataLengthSegment\t\t2\t\t%s (%d*2=%d bytes)\n" % (int_to_hexstring(int(length/2), little_endian=False, number_of_hex_digits=2), int(length/2), length)
		out += "Vertical\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3), self.vertical)
		out += "Horizontal\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3), self.horizontal)
		if self.font_style in FontStyles:
			out += "FontStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2), FontStyles[self.font_style])
		else:
			out += "FontStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		if self.draw_style in DrawStyles:
			out += "DrawStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2), DrawStyles[self.draw_style])
		else:
			out += "DrawStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		out += "Height\t\t\t\t\t4\t\t%s (%d px?)\n" % (int_to_hexstring(self.height, little_endian=False, number_of_hex_digits=4), self.height)
		out += "Width\t\t\t\t\t4\t\t%s (%d px?)\n" % (int_to_hexstring(self.width, little_endian=False, number_of_hex_digits=4), self.width)
		out += "Border?\t\t\t\t\t4\t\t%s (%d px?)\n" % (int_to_hexstring(self.border, little_endian=False, number_of_hex_digits=4), self.border)
		return out




class EntityLine:
	"""
	Line entity, no support in Demo Tool

	Part					Length	Data
	DataLengthSegment		2		07(7*2=14 bytes for lines)
	Vertical				3		010(1), 020(2), FF0(255), 001(256), FF1(511), 002(512)
	Horizontal				3		001(1), 003(3), 0FF(255), 1FF(511), 200(512)
	DrawStyle				2		00(Normal), 55(Red), AA(Red and Inversed FG BG), FF(Inverse FG BG)
	FontStyle				2		62(Hline), 63(Vline)
	Border?					4		0002(2px?) Some integer?
	"""
	def __init__(self, raw="", vertical=0, horizontal=0, draw_style=0, font_style=0, border=0):
		if len(raw) > 0:
			self._raw = raw
			self.length = hexstring_to_int(self._raw[0:2], little_endian=False)*2
			if self.length != 14:
				raise Exception(f'Rectangle package is always 2+14 byte.')
			self.vertical = hexstring_to_int(self._raw[2:5], little_endian=True)
			self.horizontal = hexstring_to_int(self._raw[5:8], little_endian=False)
			self.draw_style = hexstring_to_int(self._raw[8:10], little_endian=False)
			self.font_style = hexstring_to_int(self._raw[10:12], little_endian=False)
			self.border = hexstring_to_int(self._raw[12:16], little_endian=False)
		else:
			self.length = 0
			self.vertical = vertical
			self.horizontal = horizontal
			self.draw_style = draw_style
			self.font_style = font_style
			self.border = border
		if self.font_style not in [FontStylesInv["Horizontal Line"], FontStylesInv["Vertical Line"]]:
			raise Exception("Draw style for line must be %02X (Horizontal Line) or %02X (Vertical Line)." % (FontStylesInv["Horizontal Line"], FontStylesInv["Vertical Line"]))

	def __repr__(self):
		"""
		Build and return a line entity package
		:return: str representing entity
		"""
		# Start with packet, then add length of packet
		out = ""
		out += int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3)
		out += int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3)
		out += int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.border, little_endian=False, number_of_hex_digits=4)
		length = int_to_hexstring(int(len(out)/2), little_endian=False, number_of_hex_digits=2)
		out = length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		out = "Entity Line package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		length = len(self.__repr__())-2
		out += "DataLengthSegment\t\t2\t\t%s (%d*2=%d bytes)\n" % (int_to_hexstring(int(length/2), little_endian=False, number_of_hex_digits=2), int(length/2), length)
		out += "Vertical\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.vertical, little_endian=True, number_of_hex_digits=3), self.vertical)
		out += "Horizontal\t\t\t\t3\t\t%s (%d)\n" % (int_to_hexstring(self.horizontal, little_endian=False, number_of_hex_digits=3), self.horizontal)
		if self.draw_style in DrawStyles:
			out += "DrawStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2), DrawStyles[self.draw_style])
		else:
			out += "DrawStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.draw_style, little_endian=False, number_of_hex_digits=2)
		if self.font_style in FontStyles:
			out += "FontStyle\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2), FontStyles[self.font_style])
		else:
			out += "FontStyle\t\t\t\t2\t\t%s (Unknown)\n" % int_to_hexstring(self.font_style, little_endian=False, number_of_hex_digits=2)
		out += "Border?\t\t\t\t\t4\t\t%s (%d px?)\n" % (int_to_hexstring(self.border, little_endian=False, number_of_hex_digits=4), self.border)
		return out


class EntityLEDData:
	"""
	This enity describes how the display tag will flash after a update.

	Part					Length	Data
	DataLengthSegment		2		07(7*2=14B) Always 07 for LEDData
	FlashColor				2		01(B), 02(G), 03(BG), 04(R), 05(BR), 06(GR), 07(BGR)
	ServiceCode				4		4E31(20017)
	Hardcoded				4		00ED Hardcoded value? it always seems fixed
	FlashTimes				4		0003(3), 00FF(255), 0100(256)
	Example: 07044E2E00ED0003 blink red 3 time
	"""
	def __init__(self, raw="", color_red=False, color_green=True, color_blue=False, service_code=0, flash_times=1):
		if len(raw) > 0:
			self._raw = raw
			if len(self._raw) != 16:
				raise Exception(f'LED Data package is always a 16 byte string, this string is {len(self._raw)} Packet: {self._raw}')
			self.length = hexstring_to_int(self._raw[0:2], little_endian=False)
			flash_color = hexstring_to_int(self._raw[2:4], little_endian=False)
			if (flash_color & 1) == 1:
				self.color_red = True
			else:
				self.color_red = False
			if (flash_color & 2) == 2:
				self.color_green = True
			else:
				self.color_green = False
			if (flash_color & 4) == 4:
				self.color_blue = True
			else:
				self.color_blue = False
			self.service_code = hexstring_to_int(self._raw[4:8], little_endian=False)
			self.flash_times = hexstring_to_int(self._raw[12:16], little_endian=False)
		else:
			self.length = 0
			self.color_red = color_red
			self.color_green = color_green
			self.color_blue = color_blue
			self.service_code = service_code
			self.flash_times = flash_times

	def __repr__(self):
		"""
		Build and return a LED data package
		:return: str representing LED flash data
		"""
		flash_color = 0
		if self.color_red:
			flash_color += 1
		if self.color_green:
			flash_color += 2
		if self.color_blue:
			flash_color += 4
		# Start with packet, then add length of packet
		out = ""
		out += int_to_hexstring(flash_color, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.service_code, little_endian=False, number_of_hex_digits=4)
		out += "00ED"  # Hardcoded value? it always seems fixed
		out += int_to_hexstring(self.flash_times, little_endian=False, number_of_hex_digits=4)
		length = int_to_hexstring(int(len(out)/2), little_endian=False, number_of_hex_digits=2)
		out = length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		flash_color = 0
		flash_color_str = ""
		if self.color_red:
			flash_color += 1
			flash_color_str += "01 Red | "
		if self.color_green:
			flash_color += 2
			flash_color_str += "02 Green | "
		if self.color_blue:
			flash_color += 4
			flash_color_str += "04 Blue | "
		out = "LED Data package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		out += "DataLengthSegment\t\t2\t\t07 (7*2=14B) Always 07 for LEDData\n"
		out += "FlashColor\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(flash_color, little_endian=False,
																		number_of_hex_digits=2), flash_color_str)
		out += "ServiceCode\t\t\t\t4\t\t%s (%d)\n" % (int_to_hexstring(self.service_code, little_endian=False,
																		number_of_hex_digits=4), self.service_code)
		out += "Hardcoded\t\t\t\t4\t\t00ED Hardcoded value\n"
		out += "FlashTimes\t\t\t\t4\t\t%s (%d)\n" % (int_to_hexstring(self.flash_times, little_endian=False,
																		number_of_hex_digits=4), self.flash_times)
		return out


class Answer:
	"""
	Answer package is a response from the ESL gateway on a erlier package.
	The answer have the same service code as the earlier packet.

	Part					Length	Data
	Start					1		@
	Length					4		0012 (18 bytes length?)
	ServiceCode				4		4E23(20003) 78 35
	Display Tag ID			6		061C95
	RSSI					2		AD(173-254=-81)
	TagStatus				2		4E(Failed), 54(Success), E1(ERRE1), E2(ERRE2), E3(ERRE3), E4(ERRE4), E5(ERRE5), E6(ERRE6)
	Volt					2		1F(31=3.1V)
	Temperature				2		11(17)
	Example: @00124E23061C95AD541F17
	"""
	def __init__(self, raw="", service_code=0, display_tag_id="", rssi=0, tag_status=0, volt=0.0, temperature=0):
		if len(raw) > 0:
			self._raw = raw
			if len(self._raw) != 23:
				raise Exception(f'Answer package is always a 23 byte string, this string is {len(self._raw)} Packet: {self._raw}')
			self.length = hexstring_to_int(self._raw[1:5], little_endian=False)
			self.service_code = hexstring_to_int(self._raw[5:9], little_endian=False)
			self.display_tag_id = self._raw[9:15]
			self.rssi = hexstring_to_int(self._raw[15:17], little_endian=False)-254
			self.tag_status = hexstring_to_int(self._raw[17:19], little_endian=False)
			self.volt = float(hexstring_to_int(self._raw[19:21], little_endian=False))/10
			self.temperature = hexstring_to_int(self._raw[21:23], little_endian=False)
		else:
			self.length = 0
			self.service_code = service_code
			self.display_tag_id = display_tag_id
			self.rssi = rssi
			self.tag_status = tag_status
			self.volt = volt
			self.temperature = temperature

	def __repr__(self):
		"""
		Build and return a answer package
		:return: str representing answer package
		"""
		# Start with packet, add start and length after
		out = ""
		out += int_to_hexstring(self.service_code, little_endian=False, number_of_hex_digits=4)
		out += self.display_tag_id
		out += int_to_hexstring(self.rssi+254, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.tag_status, little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(int(self.volt*10), little_endian=False, number_of_hex_digits=2)
		out += int_to_hexstring(self.temperature, little_endian=False, number_of_hex_digits=2)
		length = int_to_hexstring(len(out), little_endian=False, number_of_hex_digits=4)
		out = '@' + length + out
		return out

	def __str__(self):
		"""
		Build a human readable packet
		:return: str
		"""
		out = "Answer package\n"
		out += "Part\t\t\t\t\tLength\tData\n"
		out += "Start\t\t\t\t\t1\t\t@\n"
		out += "Length\t\t\t\t\t4\t\t0012 (18 bytes)\n"
		out += "ServiceCode\t\t\t\t4\t\t%s (%d)\n" % (int_to_hexstring(self.service_code, little_endian=False,
																		number_of_hex_digits=4), self.service_code)
		out += "Display Tag ID\t\t\t6\t\t%s\n" % self.display_tag_id
		out += "RSSI\t\t\t\t\t2\t\t%s (%d-254=%d)\n" % (int_to_hexstring(self.rssi+254, little_endian=False,
																		number_of_hex_digits=2),
																		self.rssi+254, self.rssi)
		if self.tag_status in AnswerTagStatus:
			out += "TagStatus\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.tag_status, little_endian=False,
																		number_of_hex_digits=2),
																		AnswerTagStatus[self.tag_status])
		else:
			out += "TagStatus\t\t\t\t2\t\t%s (%s)\n" % (int_to_hexstring(self.tag_status, little_endian=False,
																		number_of_hex_digits=2),
																		"Unknown")
		out += "Volt\t\t\t\t\t2\t\t%s (%d=%.1fV)\n" % (int_to_hexstring(int(self.volt*10), little_endian=False,
																		number_of_hex_digits=2), int(self.volt*10),
																		self.volt)
		out += "Temperature\t\t\t\t2\t\t%s (%d degree Celsius)\n" % (int_to_hexstring(self.temperature,
																						little_endian=False,
																						number_of_hex_digits=2),
																						self.temperature)
		return out


# print(Answer("@00124E23061C95AD541F11").__str__())
# print(EntityLEDData("07044E2E00ED0003").__str__())
# print(EntityText("1701000100020059006F0020006D0061006D006D00610021").__str__())
# print(EntityText("0701000100020041").__str__())
# print(EntityText("09010001000200410061").__str__())
# print(EntityBarcode("0D010001004200880039003A008A").__str__())
# print(EntityBarcode("0F01000100420088003100300052008A").__str__())
# print(EntityBarcode("25010001004100880037003300310031003200350030003000300039003400310039003D008A").__str__())
# print(EntityBarcode("25010001004900880037003300310031003200350030003000300039003400310039003D008A").__str__())
# print(EntityRectangle("0B0100016400003200320001").__str__())
# print(EntityLine("0701000100620001").__str__())
