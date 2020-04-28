from unittest import TestCase

from esllib.barcode import validate_barcode128b_characters, validate_ean13_characters, \
	calculate_barcode128b_check_digit, calculate_ean13_check_digit


class TestBarcode(TestCase):
	def test_validate_barcode128b_characters_valid(self):
		self.assertTrue(validate_barcode128b_characters("asdf"))
		self.assertTrue(validate_barcode128b_characters("asdf qwerty"))
		self.assertTrue(validate_barcode128b_characters("http://tim.gremalm.se"))

	def test_validate_barcode128b_characters_invalid(self):
		self.assertFalse(validate_barcode128b_characters("asdfå"))

	def test_barcode128_checkdigit(self):
		self.assertEqual("7", calculate_barcode128b_check_digit("6"))
		self.assertEqual("8", calculate_barcode128b_check_digit("7"))
		self.assertEqual(":", calculate_barcode128b_check_digit("9"))
		self.assertEqual("R", calculate_barcode128b_check_digit("10"))
		self.assertEqual("0", calculate_barcode128b_check_digit("123456"))

	def test_validate_ean13_characters_valid(self):
		self.assertTrue(validate_ean13_characters("123456"))

	def test_validate_ean13_characters_invalid(self):
		self.assertFalse(validate_ean13_characters("123a456"))

	def test_barcode128_checkdigit(self):
		self.assertEqual("0", calculate_ean13_check_digit("746996932940"))
		self.assertEqual("1", calculate_ean13_check_digit("401234567890"))
		self.assertEqual("2", calculate_ean13_check_digit("731125000940"))
		self.assertEqual("3", calculate_ean13_check_digit("514835276686"))
		self.assertEqual("5", calculate_ean13_check_digit("831837910856"))
		self.assertEqual("4", calculate_ean13_check_digit("594874219197"))
		self.assertEqual("6", calculate_ean13_check_digit("030601215318"))
		self.assertEqual("7", calculate_ean13_check_digit("563693649095"))
		self.assertEqual("8", calculate_ean13_check_digit("919213547148"))
		self.assertEqual("9", calculate_ean13_check_digit("731125000941"))
		self.assertEqual("1", calculate_ean13_check_digit("137795146345"))
		self.assertEqual("1", calculate_ean13_check_digit("400969089062"))
