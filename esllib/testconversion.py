from unittest import TestCase
from esllib.conversion import int_to_hexstring, hexstring_to_int, utf8_to_utf16hexstring, utf16hexstring_to_utf8


class TestConversion(TestCase):
	def test_int_to_hexstring_big(self):
		self.assertEqual("0001", int_to_hexstring(number=1, little_endian=False, number_of_hex_digits=4))
		self.assertEqual("001", int_to_hexstring(number=1, little_endian=False, number_of_hex_digits=3))
		self.assertEqual("0FF", int_to_hexstring(number=255, little_endian=False, number_of_hex_digits=3))
		self.assertEqual("100", int_to_hexstring(number=256, little_endian=False, number_of_hex_digits=3))
		self.assertEqual("1FF", int_to_hexstring(number=511, little_endian=False, number_of_hex_digits=3))
		self.assertEqual("200", int_to_hexstring(number=512, little_endian=False, number_of_hex_digits=3))
		self.assertEqual("4E31", int_to_hexstring(number=20017, little_endian=False, number_of_hex_digits=4))
		self.assertEqual("00000004", int_to_hexstring(number=4, little_endian=False, number_of_hex_digits=8))
		self.assertEqual("0C0D", int_to_hexstring(number=0x0c0d, little_endian=False, number_of_hex_digits=4))
		self.assertEqual("0A0B0C0D", int_to_hexstring(number=0x0a0b0c0d, little_endian=False, number_of_hex_digits=8))

	def test_int_to_hexstring_little(self):
		self.assertEqual("0100", int_to_hexstring(number=1, little_endian=True, number_of_hex_digits=4))
		self.assertEqual("010", int_to_hexstring(number=1, little_endian=True, number_of_hex_digits=3))
		self.assertEqual("FF0", int_to_hexstring(number=255, little_endian=True, number_of_hex_digits=3))
		self.assertEqual("001", int_to_hexstring(number=256, little_endian=True, number_of_hex_digits=3))
		self.assertEqual("FF1", int_to_hexstring(number=511, little_endian=True, number_of_hex_digits=3))
		self.assertEqual("002", int_to_hexstring(number=512, little_endian=True, number_of_hex_digits=3))
		self.assertEqual("314E", int_to_hexstring(number=20017, little_endian=True, number_of_hex_digits=4))
		self.assertEqual("04000000", int_to_hexstring(number=4, little_endian=True, number_of_hex_digits=8))
		self.assertEqual("0D0C", int_to_hexstring(number=0x0c0d, little_endian=True, number_of_hex_digits=4))
		self.assertEqual("0D0C0B0A", int_to_hexstring(number=0x0a0b0c0d, little_endian=True, number_of_hex_digits=8))

	def test_hexstring_to_int_big(self):
		self.assertEqual(1, hexstring_to_int(inputstring="001", little_endian=False))
		self.assertEqual(241, hexstring_to_int(inputstring="F1", little_endian=False))
		self.assertEqual(255, hexstring_to_int(inputstring="FF", little_endian=False))
		self.assertEqual(256, hexstring_to_int(inputstring="100", little_endian=False))
		self.assertEqual(20017, hexstring_to_int(inputstring="4E31", little_endian=False))
		self.assertEqual(0x0c0d, hexstring_to_int(inputstring="0C0D", little_endian=False))
		self.assertEqual(0x0a0b0c0d, hexstring_to_int(inputstring="0A0B0C0D", little_endian=False))

	def test_hexstring_to_int_little(self):
		self.assertEqual(1, hexstring_to_int(inputstring="010", little_endian=True))
		self.assertEqual(241, hexstring_to_int(inputstring="F1", little_endian=True))
		self.assertEqual(255, hexstring_to_int(inputstring="FF", little_endian=True))
		self.assertEqual(256, hexstring_to_int(inputstring="001", little_endian=True))
		self.assertEqual(20017, hexstring_to_int(inputstring="314E", little_endian=True))
		self.assertEqual(0x0c0d, hexstring_to_int(inputstring="0D0C", little_endian=True))
		self.assertEqual(0x0a0b0c0d, hexstring_to_int(inputstring="0D0C0B0A", little_endian=True))

	def test_utf8_to_utf16hexstring(self):
		self.assertEqual("0041", utf8_to_utf16hexstring("A"))
		self.assertEqual("00410061", utf8_to_utf16hexstring("Aa"))
		self.assertEqual("0059006F0020006D0061006D006D00610021", utf8_to_utf16hexstring("Yo mamma!"))
		self.assertEqual("003100320033003400350036003700380039", utf8_to_utf16hexstring("123456789"))
		self.assertEqual("0041002000E500E400F600200042", utf8_to_utf16hexstring("A åäö B"))
		self.assertEqual("0041002000C500C400D600200042", utf8_to_utf16hexstring("A ÅÄÖ B"))
		self.assertEqual("003D007B007D005B005D00250026", utf8_to_utf16hexstring("={}[]%&"))

	def test_utf8_to_utf16hexstring(self):
		self.assertEqual("A", utf16hexstring_to_utf8("0041"))
		self.assertEqual("Aa", utf16hexstring_to_utf8("00410061"))
		self.assertEqual("Yo mamma!", utf16hexstring_to_utf8("0059006F0020006D0061006D006D00610021"))
		self.assertEqual("123456789", utf16hexstring_to_utf8("003100320033003400350036003700380039"))
		self.assertEqual("A åäö B", utf16hexstring_to_utf8("0041002000E500E400F600200042"))
		self.assertEqual("A ÅÄÖ B", utf16hexstring_to_utf8("0041002000C500C400D600200042"))
		self.assertEqual("={}[]%&", utf16hexstring_to_utf8("003D007B007D005B005D00250026"))
