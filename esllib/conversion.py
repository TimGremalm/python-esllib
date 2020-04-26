def int_to_hexstring(number: int, little_endian: bool, number_of_hex_digits: int) -> str:
	hex_string = '%X' % number
	# Validate number of digits
	if len(hex_string) > number_of_hex_digits:
		raise Exception(f'Number {number} 0x{hex_string} cant fit in {number_of_hex_digits} hexadecimal digits.')
	# Pad leading zeros
	hex_string = hex_string.rjust(number_of_hex_digits, '0')
	if little_endian:
		# Reverse order in pair of 2, from right
		hex_string_reversed = ""
		for i in range(number_of_hex_digits, 0, -2):
			hex_string_reversed += hex_string[max(0, i - 2):i]
		return hex_string_reversed
	else:
		return hex_string


def hexstring_to_int(inputstring: str, little_endian: bool) -> int:
	hexstring = ""
	if little_endian:
		# Reverse order in pair of 2, from left
		for i in range(0, len(inputstring), 2):
			hexstring = inputstring[i:i+2] + hexstring
	else:
		hexstring = inputstring
	return int(hexstring, base=16)


def utf8_to_utf16hexstring(inputstring: str) -> str:
	out = ""
	for character in inputstring:
		# Convert to UTF-16 and remove BOM flag
		utf16string = character.encode("UTF-16")[2:]
		# Convert to hexadecimal big endian
		out += "%02X%02X" % (utf16string[1], utf16string[0])
	return out


def utf16hexstring_to_utf8(inputstring: str) -> str:
	out = ""
	# For every 4 hexadecimal in string, convert to UTF-8
	for i in range(0, len(inputstring), 4):
		# Prepare UTF-16 string with BOM flag
		character = bytearray(b'\xff\xfe')
		# Extract 2 bytes and convert to int
		first = hexstring_to_int(inputstring[i+0:i+2], little_endian=False)
		second = hexstring_to_int(inputstring[i+2:i+4], little_endian=False)
		# Append to UTF-16 string in little endian
		character.append(second)
		character.append(first)
		# Decode UTF-16
		out += character.decode("UTF-16")
	return out
