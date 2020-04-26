FontStyles = {
	0x01: '7px',
	0x02: '12px',
	0x03: '16px',
	0x04: '24px',
	0x05: '32px',
	0x06: '48px',
	0x07: '64px',
	0x20: '24x12px',						# Stretched font
	0x21: '28x14px',						# Stretched font
	0x22: '32x16px',						# Stretched font
	0x23: '36x18px',						# Stretched font
	0x24: '40x20px',						# Stretched font
	0x25: '48x24px',						# Stretched font
	0x26: '56x28px',						# Stretched font
	0x27: '64x32px',						# Stretched font
	0x28: '24x9px',							# Stretched font
	0x29: '32x12px',						# Stretched font
	0x2A: '40x15px',						# Stretched font
	0x2B: '48x18px',						# Stretched font
	0x2C: '56x21px',						# Stretched font
	0x2D: '64x24px',						# Stretched font
	0x2E: '80x30px',						# Stretched font
	0x2F: '96x36px',						# Stretched font
	0x30: '112x42px',						# Stretched font
	0x31: '128x48px',						# Stretched font
	0x32: '144x48px',						# Stretched font
	0x34: '192x48px',						# Stretched font
	0x33: '160x48px',						# Stretched font
	0x40: 'Barcode EAN8',					# No support in Demo Tool
	0x41: 'Barcode EAN13',					# Start Code B 0088 : 'UTF-16 HTS',, Encoded data  : 'Ex. 0037 7 0033 3 0031 1 0031 1 0032 2 0035 5 0030 0 0030 0 0030 0 0039 9 0034 4 0031 1',, Check Digit  : 'Ex. 39 9',, Stop 003D 008A : 'UTF-16 VTS',
	0x42: 'Barcode 128',					# Start Code B 0088 : 'UTF-16 HTS',, Encoded data  : 'Ex. 0031 1, 0030 0',, Check Digit  : 'Ex. 0052 R',, Stop 008A : 'UTF-16 VTS',
	0x43: 'Barcode Code39',					# No support in Demo Tool
	0x48: 'Barcode EAN8 Double Size',		# No support in Demo Tool
	0x49: 'Barcode EAN13 Double Size',
	0x4A: 'Barcode 128 Double Size',
	0x4B: 'Barcode Code39 Double Size',
	0x50: 'Barcode EAN8 Ext',				# No support in Demo Tool
	0x51: 'Barcode EAN13 Ext',
	0x52: 'Barcode 128 Ext',
	0x53: 'Barcode Code39 Ext',				# No support in Demo Tool
	0x61: 'Horizontal Line',				# No support in Demo Tool
	0x62: 'Vertical Line',					# No support in Demo Tool
	0xFC: 'ImageCompress',
	0xFD: 'ImageX2',
	0xFE: 'Image'
}

PatternsCodes = {
	0x30: 'UpdatePart1',			# Partial update of frame buffer, useful for simple updates?
	0x31: 'DisplayID',
	0x33: 'Update1/Screen1',		# Write to frame buffer 1
	0x34: 'NoUpdate1',
	0x35: 'Display1',				# Display frame buffer 1
	0x36: 'Update2/Screen2',		# Write to frame buffer 2
	0x37: 'NoUpdate2',
	0x38: 'Display2',				# Display frame buffer 2
	0x39: 'Update3/Screen3',		# Write to frame buffer 3
	0x3A: 'NoUpdate3',
	0x3B: 'Display3',				# Display frame buffer 3
	0x3C: 'Update4/Screen4',		# Write to frame buffer 4
	0x3D: 'NoUpdate4',
	0x3E: 'Display4',				# Display frame buffer 4
	0x42: 'Frosted',
	0x43: 'UpdatePart2',
	0x44: 'UpdatePart3',
	0x45: 'UpdatePart4',
	0x47: 'Version',
	0x49: 'Key',
	0x53: 'Bind'
}

AnswerTagStatus = {0x4E: 'Failed',
					0x54: 'Success',
					0xE1: 'ERRE1',
					0xE2: 'ERRE2',
					0xE3: 'ERRE3',
					0xE4: 'ERRE4',
					0xE5: 'ERRE5',
					0xE6: 'ERRE6'
}
