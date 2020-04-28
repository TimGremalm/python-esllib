# https://en.wikipedia.org/wiki/Code_128
barcode_128_b_characters = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']


def validate_barcode128b_characters(inputstring: str) -> bool:
	"""
	It seems that only Code 128 B characters are supported on the ESL displays.
	This function validates that characters in inputstring is valid.

	:param inputstring: str to validate
	:return: bool True if valid
	"""
	for character in inputstring:
		if character not in barcode_128_b_characters:
			return False
	return True


def calculate_barcode128b_check_digit(inputstring: str) -> str:
	"""
	Calculates the check digit for Barcode 128 B.
	https://en.wikipedia.org/wiki/Code_128#Check_digit_calculation

	:param inputstring: str to calculate
	:return: 1 single character representing the check digit
	"""
	sum = 104  # Start Code B
	for count, character in enumerate(inputstring):
		value = barcode_128_b_characters.index(character)
		sum += value * (count+1)
	check_digit = sum % 103
	return chr(check_digit + 32)


def validate_ean13_characters(inputstring: str) -> bool:
	"""
	EAN only supports numbers.
	This function validates that characters in inputstring is valid.

	:param inputstring: str to validate
	:return: bool True if valid
	"""
	for character in inputstring:
		if character not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
			return False
	return True


def calculate_ean13_check_digit(inputstring: str) -> str:
	"""
	Calculates the check digit for EAN 13.
	https://en.wikipedia.org/wiki/International_Article_Number#Calculation_of_checksum_digit

	:param inputstring: str to calculate
	:return: 1 single character representing the check digit
	"""
	checksum = 0
	for count, character in enumerate(inputstring):
		# odd data digits are always weight of 3 and the even data digits are always weight of 1
		if (count % 2) == 0:
			weight = 1
		else:
			weight = 3
		checksum += weight * int(character)
	check_digit = 10 - (checksum % 10)
	if check_digit == 10:
		return '0'
	else:
		return '%d' % check_digit
