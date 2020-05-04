from PIL import Image


def int_to_hexstring(number: int, little_endian: bool, number_of_hex_digits: int) -> str:
	"""
	Converts a integer to a hexadecimal string
	:param number: int to be converted
	:param little_endian: bool True if hexadecimal string is to be formated in little endian
	:param number_of_hex_digits: int number of hexadecimal digits  in string
	:return: hexadecimal string
	"""
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
	"""
	Converts a hexadecimal coded string to a integer
	:param inputstring: str to be decoded
	:param little_endian: bool True to decode string as little endian
	:return: int
	"""
	hexstring = ""
	if little_endian:
		# Reverse order in pair of 2, from left
		for i in range(0, len(inputstring), 2):
			hexstring = inputstring[i:i+2] + hexstring
	else:
		hexstring = inputstring
	return int(hexstring, base=16)


def utf8_to_utf16hexstring(inputstring: str) -> str:
	"""
	Convert UTF-8 characters to UTF-16 coded hexadecimal string big endian
	:param inputstring: str to be converted
	:return: str hexadecimal string
	"""
	out = ""
	for character in inputstring:
		# Convert to UTF-16 and remove BOM flag
		utf16string = character.encode("UTF-16")[2:]
		# Convert to hexadecimal big endian
		out += "%02X%02X" % (utf16string[1], utf16string[0])
	return out


def utf16hexstring_to_utf8(inputstring: str) -> str:
	"""
	Convert hexadecimal sting of UTF-16 encoded characters to UTF-8 string
	:param inputstring: str to be converted
	:return: str UTF-8
	"""
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


def catogerize_rgb_as_color(red: int, green: int, blue: int) -> str:
	if red < 128 and green < 128 and blue < 128:
		# if red, green and blue is less then mid, treat it as a black pixel
		return 'black'
	elif red > 127 and green > 127 and blue < 128:
		# if red and green is above mid and blue is below, treat it as a yellow pixel
		return 'yellow'
	elif red > 127 and green < 128 and blue < 128:
		# if red is above mid and the rest is below, treat it as a red pixel
		return 'red'
	else:
		return 'white'


def image_to_black_and_colored_pixel_strings(image: Image) -> (list, list):
	"""
	Analyze colors in Pillow image, return a tuple of pixel array matching black pixels,
	and a pixel array matching red/yellow pixels.
	E-ink is a passive display, so we want to mark out all black and potentially red/yellow pixels to draw.
	The color of the colored array doesn't matter since the e-ink displays pnly support a optional second color like
	red or yellow.
	The two string arrays shall be equally long, and represent the amount od pixels in the image.

	:param image: Pillow Image extract pixels from
	:return: (list, list) a tuple concisting of a list matching black pixels, and colored pixels
	"""
	pixels_black = []
	pixels_color = []
	pixel_access = image.load()  # Used for reading pixel value of a Pillow image
	for y in range(image.height):
		for x in range(image.width):
			r, g, b = pixel_access[x, y]
			color = catogerize_rgb_as_color(r, g, b)
			if color == 'black':
				pixels_black.append(1)
				pixels_color.append(0)
			elif color == 'yellow' or color == 'red':
				pixels_black.append(0)  # Don't color in black pixels since we are going to draw a colored
				pixels_color.append(1)
			else:
				pixels_black.append(0)
				pixels_color.append(0)
	return pixels_black, pixels_color


def compress_pixel_array(inputstring: list) -> str:
	"""

	:param inputstring: list of ints representing pixels to compress
	:return: str compressed
	"""
	pixel_counter = 0
	pixel_counter_offset = 0
	compressed_pixels = ""
	# Loop through image to be compressed
	while pixel_counter < len(inputstring):
		pixel = inputstring[pixel_counter]
		count_until_colorchange = 0
		# Count until pixel change color, or we hit 65535, or reach end of image
		while pixel == inputstring[pixel_counter + count_until_colorchange]:
			count_until_colorchange += 1
			if pixel_counter + count_until_colorchange >= len(inputstring):
				# Don't try to read more pixels then there is pixels available
				break
			if count_until_colorchange >= 65535:
				# Don't try to read more pixels than can be fitted in to 2 bytes length
				break

		# Decide how to compress
		if count_until_colorchange < 7:
			# If number of same pixels is less than a byte, fill it up with pixel pattern
			# Bit pattern 1 byte (1 for pixel pattern, pattern)
			# 0xC0(0b11000000) 1 black pixel, 5 white pixels
			# 0xE0(0b11100000) 2 black pixels, 4 white pixels
			pixel_pattern = (1 << 7)
			# Build pixel pattern usings remaining bits of the byte
			for i in range(7):
				if pixel_counter + i >= len(inputstring):
					break  # Don't read outside of image size
				pixel_pattern = pixel_pattern | (inputstring[pixel_counter+i] << (6-i))
			compressed_pixels += int_to_hexstring(pixel_pattern, little_endian=False, number_of_hex_digits=2)
			pixel_counter += 7
		elif count_until_colorchange <= 31:
			# Short color string 1 byte (0 for color string, pixel type, number of pixels])
			# 0x47 0b01000111 0b111 = 7 black pixels
			# 0x1F 0b00011111 0b11111 = 31 white pixels
			value = (0 << 7) + (pixel << 6) + count_until_colorchange
			compressed_pixels += int_to_hexstring(value, little_endian=False, number_of_hex_digits=2)
			pixel_counter += count_until_colorchange
		elif count_until_colorchange <= 255:
			# Middle color string 2 bytes (0 for color string, pixel type, 000001 for 1B length) (number of pixels])
			# 0x01(0b00000001) 0x20(0b00010100) 32 white pixels
			# 0x41(0b01000001) 0x20(0b00010100) 32 black pixels
			value = (0 << 7) + (pixel << 6) + 1
			compressed_pixels += int_to_hexstring(value, little_endian=False, number_of_hex_digits=2)
			compressed_pixels += int_to_hexstring(count_until_colorchange, little_endian=False, number_of_hex_digits=2)
			pixel_counter += count_until_colorchange
		else:
			# Long color string 3 bytes (0 for color string, pixel type, 000000 for 2B length) (number of pixels little endian]) (number of pixels big endian])
			# 0x00(0b00000000) 0xBA 0xD4 54458 white pixels
			# 0x40(0b01000000) 0x00 0x01 256 black pixels
			value = (0 << 7) + (pixel << 6) + 0
			compressed_pixels += int_to_hexstring(value, little_endian=False, number_of_hex_digits=2)
			compressed_pixels += int_to_hexstring(count_until_colorchange, little_endian=True, number_of_hex_digits=4)
			pixel_counter += count_until_colorchange
	return compressed_pixels
