from esllib.conversion import int_to_hexstring, hexstring_to_int, utf8_to_utf16hexstring, utf16hexstring_to_utf8
from esllib.enums import AnswerTagStatus


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
