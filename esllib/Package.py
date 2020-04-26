from esllib.conversion import int_to_hexstring, hexstring_to_int, utf8_to_utf16hexstring, utf16hexstring_to_utf8


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
		:return: string representing answer package
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
		return ""
